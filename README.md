# My BitBar Scripts

Here are my Python scripts and a library for [BitBar][bitbar-home].

## Usage

Create a soft link from `scripts` to enabled
```bash
ln -s scripts/XXX.py enabled/XXX.??m.py
```
or just copy it there.

## The Library

The [`libs/bitbar.py`](/libs/bitbar.py) automates the generation of output.

Simply create a `BitBarMessagePack` and `append()` any message to it, attributes like color, font or href is attached as a `dict`.

### Examples

Further examples refer to published scripts.

#### Multi-line plugin with extra data

```bash
#!/bin/bash
echo "One"
echo "Two"
echo "Three"
echo "---"
echo "Four"
echo "Five"
echo "Six"
```
equals
```python
pkg = BitBarMessagePack("One\nTwo\nThree")
echo "---"
pkg.append("Four")
pkg.append(Five")
pkg.append("Six")
```

## Scripts

### [📺 Slurm Queue](/scripts/squeue.py)

List [Slurm][slurm] queue on a HPC.

<img src="/screenshots/squeue.png" width=300>

#### Requires

[`fabric`][fabfile]

#### Edit

```python
user = "USER"
server = "example.com"
prefix = ""
```

[fabfile]: http://www.fabfile.org
[slurm]: https://slurm.schedmd.com/squeue.html

### [🦠 nCov-2019 Statistics in NYC](/scripts/nCov-2019-NYC.py)

### [😷 nCov-2019 Statistics in China](/scripts/nCov-2019-CHN.py)

数据来源[丁香园][dxy-ncov]。

[dxy-ncov]: https://ncov.dxy.cn/ncovh5/view/pneumonia

[bitbar-home]: https://getbitbar.com
[bitbar-github]: https://github.com/matryer/bitbar
