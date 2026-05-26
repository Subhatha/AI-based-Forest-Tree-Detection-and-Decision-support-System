def generate_summary(stats, frame_count):
    total = stats.get("total", 0)
    cut = stats.get("cut", 0)
    keep = stats.get("keep", 0)

    cut_percent = (cut / total * 100) if total > 0 else 0
    keep_percent = (keep / total * 100) if total > 0 else 0

    summary = {
        "frames": frame_count,
        "total": total,
        "cut": cut,
        "keep": keep,
        "cut_percent": round(cut_percent, 2),
        "keep_percent": round(keep_percent, 2)
    }

    return summary


def save_summary(summary, output_path):
    with open(output_path, "w") as file:
        file.write("AI Forest Tree Detection System Report\n")
        file.write("-------------------------------------\n")
        file.write(f"Frames processed: {summary['frames']}\n")
        file.write(f"Total tree detections: {summary['total']}\n")
        file.write(f"Trees marked CUT: {summary['cut']}\n")
        file.write(f"Trees marked KEEP: {summary['keep']}\n")
        file.write(f"CUT percentage: {summary['cut_percent']}%\n")
        file.write(f"KEEP percentage: {summary['keep_percent']}%\n")