package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"sync"

	"net/http"
	"time"

	"github.com/shirou/gopsutil/v4/cpu"
	"github.com/shirou/gopsutil/v4/disk"
	"github.com/shirou/gopsutil/v4/host"
	"github.com/shirou/gopsutil/v4/mem"

	"github.com/docker/docker/api/types/container"
	"github.com/docker/docker/client"
)

var AUTH_KEY, authKeySet = os.LookupEnv("AUTH_KEY")

var (
	latestMetrics ServerMetrics
	metricsMutex  sync.RWMutex
)

type userAgentRoundTripper struct {
	rt        http.RoundTripper
	userAgent string
}
type dockerContainer struct {
	Name  string  `json:"name"`
	ID    string  `json:"id"`
	RAM   uint64  `json:"ram"`
	CPU   float32 `json:"cpu"`
	STATE string  `json:"state"`
	IMAGE string  `json:"image"`
}

type MemoryMetrics struct {
	Total     uint64 `json:"total"`
	Available uint64 `json:"available"`
	Used      uint64 `json:"used"`
	Free      uint64 `json:"free"`
	Active    uint64 `json:"active"`
	Inactive  uint64 `json:"inactive"`
	Wired     uint64 `json:"wired"`
}

type CPUMetrics struct {
	Usage float64 `json:"usage"`
}

type DockerMetrics struct {
	Stats []dockerContainer `json:"stats"`
}

type ServerMetrics struct {
	Memory MemoryMetrics   `json:"memory"`
	Host   host.InfoStat   `json:"host"`
	CPU    CPUMetrics      `json:"cpu"`
	Disk   *disk.UsageStat `json:"disk"`
	Docker DockerMetrics   `json:"docker"`
}

func authMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		authKey := r.Header.Get("AUTHKEY")
		if authKey != AUTH_KEY || !authKeySet {
			http.Error(w, "Unauthorized", http.StatusUnauthorized)
			return
		}
		next.ServeHTTP(w, r)
	})
}

func main() {
	// Initial collection of metrics
	metricsMutex.Lock()
	latestMetrics = collectMetrics()
	metricsMutex.Unlock()

	// Start background goroutine to collect metrics periodically
	go func() {
		ticker := time.NewTicker(30 * time.Second)
		defer ticker.Stop()
		for range ticker.C {
			metricsMutex.Lock()
			latestMetrics = collectMetrics()
			metricsMutex.Unlock()
		}
	}()

	http.HandleFunc("/api/server/metrics", authMiddleware(func(w http.ResponseWriter, r *http.Request) {
		metricsMutex.RLock() // Use RLock for reading
		currentMetrics := latestMetrics
		metricsMutex.RUnlock()

		w.Header().Set("Content-Type", "application/json")
		jsonBytes, err := json.Marshal(currentMetrics)
		if err != nil {
			http.Error(w, "Error marshaling JSON", http.StatusInternalServerError)
			fmt.Printf("Error marshaling JSON: %v\n", err)
			return
		}
		fmt.Fprint(w, string(jsonBytes))
	}))

	http.ListenAndServe(":8080", nil)
}

func collectMetrics() ServerMetrics {
	var (
		memStats   *mem.VirtualMemoryStat
		hostInfo   *host.InfoStat
		cpuPercent []float64
		diskUsage  *disk.UsageStat
		err        error
	)

	if memStats, err = mem.VirtualMemory(); err != nil {
		fmt.Printf("Error getting memory stats: %v\n", err)
		memStats = &mem.VirtualMemoryStat{}
	}

	if hostInfo, err = host.Info(); err != nil {
		fmt.Printf("Error getting host info: %v\n", err)
		hostInfo = &host.InfoStat{}
	}

	if cpuPercent, err = cpu.Percent(1*time.Second, false); err != nil {
		fmt.Printf("Error getting CPU usage: %v\n", err)
		cpuPercent = []float64{0.0}
	}

	if diskUsage, err = disk.Usage("/"); err != nil {
		fmt.Printf("Error getting disk usage: %v\n", err)
		diskUsage = &disk.UsageStat{}
	}

	dockerStats := getDockerStats()

	return ServerMetrics{
		Memory: MemoryMetrics{
			Total:     memStats.Total,
			Available: memStats.Available,
			Used:      memStats.Used,
			Free:      memStats.Free,
			Active:    memStats.Active,
			Inactive:  memStats.Inactive,
			Wired:     memStats.Wired,
		},
		Host: *hostInfo,
		CPU: CPUMetrics{
			Usage: func() float64 {
				if len(cpuPercent) > 0 {
					return cpuPercent[0]
				}
				return 0.0
			}(),
		},
		Disk: diskUsage,
		Docker: DockerMetrics{
			Stats: dockerStats,
		},
	}
}

func getDockerStats() []dockerContainer {
	apiClient, err := client.NewClientWithOpts(client.WithAPIVersionNegotiation())
	if err != nil {
		panic(err)
	}
	defer apiClient.Close()

	containers, err := apiClient.ContainerList(context.Background(), container.ListOptions{All: true})
	if err != nil {
		panic(err)
	}

	var (
		wg       sync.WaitGroup
		mu       sync.Mutex
		allStats []dockerContainer
	)

	for _, ctr := range containers {
		wg.Add(1)
		go func(ctr container.Summary) {
			defer wg.Done()
			stats, err := apiClient.ContainerStatsOneShot(context.Background(), ctr.ID)
			if err != nil {
				fmt.Printf("Error getting stats for container %s: %v\n", ctr.ID, err)
				return
			}
			defer stats.Body.Close()

			data, err := io.ReadAll(stats.Body)
			if err != nil {
				fmt.Printf("Error reading stats body for container %s: %v\n", ctr.ID, err)
				return
			}

			statsJSON := container.StatsResponse{}
			err = json.Unmarshal(data, &statsJSON)
			if err != nil {
				fmt.Printf("Error unmarshaling stats JSON for container %s: %v\n", ctr.ID, err)
				return
			}

			cpuDelta := float64(statsJSON.CPUStats.CPUUsage.TotalUsage) - float64(statsJSON.PreCPUStats.CPUUsage.TotalUsage)
			systemDelta := float64(statsJSON.CPUStats.SystemUsage) - float64(statsJSON.PreCPUStats.SystemUsage)

			cpuPercent := 0.0
			if systemDelta > 0.0 && cpuDelta > 0.0 {
				cpuPercent = (cpuDelta / systemDelta) * 100.0 * 7
			}

			containerStat := dockerContainer{
				Name:  statsJSON.Name[1:],
				ID:    statsJSON.ID,
				CPU:   float32(cpuPercent),
				RAM:   statsJSON.MemoryStats.Usage,
				STATE: ctr.State,
				IMAGE: ctr.Image,
			}

			mu.Lock()
			allStats = append(allStats, containerStat)
			mu.Unlock()

		}(ctr)
	}
	wg.Wait()
	return allStats
}
