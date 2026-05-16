from pathlib import Path

from scan.engine import ScanResult


def generate_markdown(result: ScanResult) -> str:
    lines = [
        f"# AutoRecon — Relatório de Varredura",
        f"",
        f"| Campo | Valor |",
        f"|-------|-------|",
        f"| **Alvo** | `{result.target}` |",
        f"| **Perfil** | `{result.profile}` |",
        f"| **Início** | {result.started_at.strftime('%Y-%m-%d %H:%M:%S')} |",
        f"| **Término** | {result.finished_at.strftime('%Y-%m-%d %H:%M:%S') if result.finished_at else '—'} |",
        f"| **Duração total** | {result.duration:.1f}s |",
        f"| **Etapas executadas** | {len(result.steps)} |",
        f"",
    ]

    success_count = sum(1 for s in result.steps if s.success)
    fail_count = len(result.steps) - success_count
    lines += [
        f"## Resumo",
        f"",
        f"- Etapas com sucesso: **{success_count}**",
        f"- Etapas com falha: **{fail_count}**",
        f"",
    ]

    lines.append("## Resultados por Etapa")
    lines.append("")

    for i, step in enumerate(result.steps, 1):
        status = "OK" if step.success else f"ERRO (rc={step.returncode})"
        lines += [
            f"### {i}. {step.label}",
            f"",
            f"- **Ferramenta:** `{step.tool}`",
            f"- **Modo:** `{step.mode}`",
            f"- **Status:** {status}",
            f"- **Duração:** {step.duration:.1f}s",
            f"- **Comando:** `{' '.join(step.command)}`",
            f"",
        ]
        if step.stdout.strip():
            lines += [
                "**Saída:**",
                "",
                "```",
                step.stdout.strip(),
                "```",
                "",
            ]
        if step.stderr.strip():
            lines += [
                "**Stderr:**",
                "",
                "```",
                step.stderr.strip(),
                "```",
                "",
            ]

    return "\n".join(lines)


def save_report(result: ScanResult, output_path: Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(generate_markdown(result))
    return output_path
