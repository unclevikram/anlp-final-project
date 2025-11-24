import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


AAEC_COMP_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../../analysis_outputs/aaec_stance_comparison.json",
    )
)


def plot_grouped_bar(pro_mean, con_mean, metric_name, out_dir):
    labels = ['pro', 'con']
    values = [pro_mean, con_mean]
    colors = ['#4C78A8', '#F58518']
    plt.figure(figsize=(4, 3))
    plt.bar(labels, values, color=colors)
    plt.title(metric_name.replace('_', ' '))
    plt.ylabel(metric_name)
    plt.tight_layout()
    out_path = os.path.join(out_dir, f"aaec_{metric_name}.png")
    plt.savefig(out_path, dpi=150)
    plt.close()
    return out_path


def main():
    with open(AAEC_COMP_PATH, encoding='utf-8') as f:
        comp = json.load(f)
    overall = comp.get('overall', {})
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../reports/figures"))
    os.makedirs(out_dir, exist_ok=True)

    paths = []
    for metric in ["attack_ratio", "evidence_density", "avg_breadth"]:
        o = overall.get(metric, {})
        pro_mean = o.get('pro_mean', 0.0)
        con_mean = o.get('con_mean', 0.0)
        paths.append(plot_grouped_bar(pro_mean, con_mean, metric, out_dir))

    print("Saved plots:\n" + "\n".join(paths))


if __name__ == "__main__":
    main()



