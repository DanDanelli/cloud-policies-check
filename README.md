# cloud-policies-check

Repositório central de políticas de segurança da organização para Checkov.

## Estrutura

```
cloud-policies-check/
├── .checkov.yml              # Configuração central (rigor via CHECKOV_LEVEL)
├── .checkov.baseline         # Baseline de violações aceitas
├── checks/terraform/         # Custom checks Python
├── tests/                    # Unit tests das custom checks
├── docs/                     # Documentação por custom policy
├── scripts/run-checkov.sh    # Wrapper de rigor adaptativo
└── .github/workflows/        # Validação e release automáticos
```

## Como consumir

Os pipelines dos repositórios de workload clonam este repo e usam o script wrapper:

```bash
git clone https://x-access-token:$TOKEN@github.com/org/cloud-policies-check.git
CHECKOV_LEVEL=non-prd cloud-policies-check/scripts/run-checkov.sh ./infra
```

## Rigor por ambiente (D-06)

| Severidade | Sandbox | Non-Prd | Prd |
|------------|---------|---------|-----|
| CRITICAL (Cat. A) | Hard-fail | Hard-fail | Hard-fail |
| HIGH | Soft-fail | Hard-fail | Hard-fail |
| MEDIUM | Soft-fail | Soft-fail | Hard-fail |
| LOW | Informativo | Informativo | Soft-fail |

## Como adicionar uma nova custom policy

1. Criar check em `checks/terraform/nome_do_check.py`
2. Criar test em `tests/test_nome_do_check.py`
3. Documentar em `docs/CKV_CUSTOM_NNN.md`
4. Abrir PR → policy-validation.yml valida automaticamente
5. Após merge → policy-release.yml cria tag semântica
