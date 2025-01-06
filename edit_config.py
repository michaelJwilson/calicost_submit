import os
import pprint
from pathlib import Path

"""
Updates pre-exisiting config files from the CalicoST simulation runs 
to achieve the desired settings and environment.

Key values to be updated:

- 'filtergenelist_file': '/n/fs/ragr-data/users/congma/references/cellranger_refdata-gex-GRCh38-2020-A/genes/ig_gene_list.txt',
- 'filterregion_file': '/n/fs/ragr-data/users/congma/references/cellranger_refdata-gex-GRCh38-2020-A/genes/HLA_regions.bed',
- 'geneticmap_file': '/u/congma/ragr-data/users/congma/Codes/CalicoST/resources/genetic_map_GRCh38_merged.tab',
- 'hgtable_file': '/u/congma/ragr-data/users/congma/Codes/STARCH_crazydev/hgTables_hg38_gencode.txt',
- 'snp_dir': '/u/congma/ragr-data/users/congma/Datasets/CalicoST_simulation/simulated_data_related/numcnas1.2_cnasize1e7_ploidy2_random0',
- 'spaceranger_dir': '/u/congma/ragr-data/users/congma/Datasets/CalicoST_simulation/simulated_data_related/numcnas1.2_cnasize1e7_ploidy2_random0',

- ** 'output_dir': '/u/congma/ragr-data/users/congma/Datasets/CalicoST_simulation/nomixing_calicost_related/numcnas1.2_cnasize1e7_ploidy2_random0',
"""

__to_patch = ("filtergenelist_file", "filterregion_file", "geneticmap_file", "hgtable_file")

def find_configs(root):
    """
    Find the pre-existing configuration files by walking a 
    given root directory.
    """
    configs = []
    
    for dirpath, dirnames, filenames in os.walk(root):
        for filename in filenames:
            if "configfile" in filename:
                configs.append(os.path.join(dirpath, filename))

    print(f"Found {len(configs)} configs.")
                
    return sorted(configs)


def read_config(fpath):
    """
    Read the configuration as key, value pairs, i.e. as
    a dictionary / hash map.
    """
    print(f"Reading config @ {fpath}")
    
    config_dict = {}
    
    with open(fpath, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            
            key, value = line.split(":", 1)
            config_dict[key.strip()] = value.strip()
            
    return config_dict


def write_config(config, opath):
    with open(opath, "w") as oo:
        for key, value in config.items():
            oo.write(f"{key} : {value}\n")

            
if __name__ == "__main__":
    repo = "/home/mw9568/repos/CalicoST"

    # NB zenodo simulation download    
    root = "/scratch/network/mw9568/zenodo"
    sim_dir = f"{root}/CalicoST_simulation_deposit/simulated_data_related"

    # NB relative path to the CalicoST results for each simulation run.
    spath = "CalicoST_simulation_deposit/nomixing_calicost_related/"

    configs = find_configs(f"{root}/{spath}")

    pprint.pprint(configs)

    proceed = input("Proceed with new config generation? [Y/N] ").strip().upper() == "Y"

    if not proceed:
        exit(0)

    # EG numcnas1.2_cnasize1e7_ploidy2_random0
    for fpath in configs:
        # NB the simulation realization
        seed = fpath[-1]
        simid = Path(fpath).parent.name
        
        config = read_config(fpath)
        config["output_dir"] = f"/scratch/network/mw9568/Calicost/bafonly/{simid}"

        # NB re-assign where to find required supplementary files.
        config["filtergenelist_file"] = f"{repo}/GRCh38_resources/ig_gene_list.txt"
        config["filterregion_file"] = f"{repo}/GRCh38_resources/HLA_regions.bed"
        config["geneticmap_file"] = f"{repo}/GRCh38_resources/genetic_map_GRCh38_merged.tab.gz"
        config["hgtable_file"] = f"{repo}/GRCh38_resources/hgTables_hg38_gencode.txt"

        config["snp_dir"] = f"{sim_dir}/{simid}"
        config["spaceranger_dir"] = f"{sim_dir}/{simid}"

        # NB re-assign to the desired settings.
        config["bafonly"] = "False"
        config["n_clones_baf"] = 3
        config["n_clones_rdr"] = 1
        
        # pprint.pprint(config)

        Path(f"{config['output_dir']}").mkdir(parents=True, exist_ok=True)

        print(f"Writing {config['output_dir']}/configfile{seed}")
        
        write_config(config, f"{config['output_dir']}/configfile{seed}")
