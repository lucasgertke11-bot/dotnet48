# .NET Framework 4.8 Portable Installer for Wine/Proton

Instala o .NET Framework 4.8 completo em qualquer prefixo Wine/Proton **sem usar winetricks**.

## Download

**[install-dotnet48.exe](https://github.com/lucasgertke11-bot/dotnet48/releases/download/v1.0.0/install-dotnet48.exe)** (265 MB)

## Uso

```bash
wget https://github.com/lucasgertke11-bot/dotnet48/releases/download/v1.0.0/install-dotnet48.exe
WINEPREFIX=/caminho/do/prefixo wine install-dotnet48.exe
```

## O que instala

- .NET Framework 4.8 completo (Framework 32/64-bit)
- Global Assembly Cache (GAC)
- mscoree.dll no system32/syswow64
- Todas as chaves de registro do .NET

## Build do instalador

```bash
# Instalar NSIS (Arch Linux)
yay -S nsis

# Compilar
cd installer
wine makensis.exe install.nsi
```

## Estrutura

```
├── installer/
│   ├── install.nsi       # Script NSIS do instalador
│   └── 7za.exe           # 7-Zip CLI (extrai o pacote)
├── registry/
│   └── dotnet48-full.reg # Registry completo do .NET 4.8
└── tools/
    └── filter-dotnet-registry.py  # Script p/ filtrar registry
```

## Licença

MIT
