import re
import matplotlib.pyplot as plt
import numpy as np

def parse_logs(log_file):
    request_processed = []

    with open(log_file, "r") as f:
        for line in f:
            # 요청 처리 데이터 추출
            if "processed in" in line:
                match = re.search(r"request: #(\d+) processed in ([\d.]+)ms", line)
                if match:
                    request_id = int(match.group(1))
                    processing_time = float(match.group(2))
                    request_processed.append((request_id, processing_time))

    return request_processed

def analyze_logs(processed, num_bins=3):
    intervals = []
    for i in range(len(processed) - 1):
        current_request = processed[i]
        next_request = processed[i + 1]

        interval = abs(next_request[1] - current_request[1])
        intervals.append(interval)

    bins = np.linspace(0, 50, num_bins + 1)  # 0~50ms를 자동으로 num_bins 개 구간으로 나눔
    bin_labels = [f"{int(bins[i])}-{int(bins[i + 1])}ms" for i in range(len(bins) - 1)]
    bin_colors = ['green', 'blue', 'red', 'purple', 'orange']

    bin_counts = []
    bin_data = []
    for i in range(len(bins) - 1):
        data = [x for x in intervals if bins[i] <= x < bins[i + 1]]
        bin_data.append(data)
        bin_counts.append(len(data))

    total_count = sum(bin_counts)

    # 서브플롯 생성
    fig, axes = plt.subplots(1, num_bins, figsize=(5 * num_bins, 5), constrained_layout=True)

    for i, ax in enumerate(axes):
        percentage = (bin_counts[i] / total_count) * 100 if total_count > 0 else 0
        ax.hist(
            bin_data[i],
            bins=20,
            alpha=0.7,
            color=bin_colors[i % len(bin_colors)],
            label=f"{bin_labels[i]} ({bin_counts[i]} packets, {percentage:.1f}%)"
        )
        ax.set_title(f"{bin_labels[i]} Interval")
        ax.set_xlabel("Processing Time Difference (ms)")
        ax.set_ylabel("Frequency")
        ax.legend()

    # 메인 제목
    fig.suptitle("Processing Time Differences by Interval", fontsize=16)
    plt.show()

if __name__ == "__main__":
    log_file = "/Users/kimjihe/Desktop/git/gRPC_Test/gRPC_project/server.log"
    processed = parse_logs(log_file)
    analyze_logs(processed, num_bins=3)  

