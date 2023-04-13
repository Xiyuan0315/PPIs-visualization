from pathlib import Path
from logger import log

root = Path.cwd().parent
logger = log.setup_custom_logger('root')
logger.debug(f"Your current working dictionary {root}")


input_dir = root / "Data"
#output_dir =root / "Output"
#if not output_dir.exists():
#    Path.mkdir(output_dir)
#    logger.info("Creat Ouput Dictionary")

