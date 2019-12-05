>Step 1, download stable version from [ref_download_pipeline](https://github.com/braveHUI/ref_download_pipeline.git), untar package

```Bash
git clone https://github.com/braveHUI/ref_download_pipeline.git
```

>Step 2, conda create ref_download_pipeline

```Bash
conda create -n ref_download_pipeline python=3
source activate ref_download_pipeline
pip install -r requirement.txt
```

>Step 2, conda create sankemake

```Bash
conda install -c bioconda -c conda-forge snakemake
```
