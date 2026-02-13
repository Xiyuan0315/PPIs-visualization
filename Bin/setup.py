from pathlib import Path
from logger import log

# Resolve project root from this file location so runtime CWD does not matter.
root = Path(__file__).resolve().parent.parent
logger = log.setup_custom_logger('ppi_visualization')
logger.debug(f"Your current working dictionary {root}")


input_dir = root / "Data"
#output_dir =root / "Output"
#if not output_dir.exists():
#    Path.mkdir(output_dir)
#    logger.info("Creat Ouput Dictionary")
