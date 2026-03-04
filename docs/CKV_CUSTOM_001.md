# CKV_CUSTOM_001 — Enforce Mandatory Tags

| Campo | Valor |
|-------|-------|
| **Rule ID** | CKV_CUSTOM_001 |
| **Severity** | HIGH |
| **Categoria** | B |
| **Framework** | Terraform |
| **Resources** | aws_instance, aws_s3_bucket, aws_rds_cluster, aws_vpc, aws_security_group, ... |

## Descrição

Todas as resources AWS que suportam tags **devem** conter as seguintes tags obrigatórias:

- `Environment` — sandbox, non-prd, prd
- `Owner` — email do time responsável
- `Project` — nome do projeto
- `CostCenter` — centro de custo para billing
- `ManagedBy` — terraform ou manual

## Justificativa

Tags consistentes são fundamentais para:
- **Cost allocation**: identificar custos por projeto/equipe
- **Automação**: scripts de cleanup, backup scheduling
- **Compliance**: auditoria e governance
- **Operações**: identificar owner em caso de incidentes

## Exemplo Compliant

```hcl
resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Environment = "prd"
    Owner       = "team-alpha@company.com"
    Project     = "project-alpha"
    CostCenter  = "CC-1234"
    ManagedBy   = "terraform"
  }
}
```

## Exemplo Non-Compliant

```hcl
resource "aws_instance" "app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t3.micro"

  tags = {
    Name = "my-instance"  # Faltam tags obrigatórias
  }
}
```
