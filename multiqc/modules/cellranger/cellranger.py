import logging

from multiqc.base_module import BaseMultiqcModule, ModuleNoSamplesFound

from .count import parse_count_html
from .vdj import parse_vdj_html

log = logging.getLogger(__name__)


class MultiqcModule(BaseMultiqcModule):
    """
    The module summarizes the main information useful for QC, including:

    - sequencing metrics
    - mapping metrics
    - estimated number of cells and reads / cell
    - UMI counts
    - mean detect genes per cell
    - antibody cell counts and distribution

    Note that information such as clustering and differential expression are not reported.

    The input files are web summaries generated by Cell Ranger. Expected file names are `*web_summary.html`.
    Sample IDs are parsed directly from the reports and the module will automatically recognize if they are
    generated from VDJ or count analysis.

    If present in the original report, any warning is reported as well.
    """

    def __init__(self):
        super(MultiqcModule, self).__init__(
            name="Cell Ranger",
            anchor="cellranger",
            href="https://support.10xgenomics.com/single-cell-gene-expression/software/pipelines/latest/what-is-cell-ranger",
            info="Analyzes single cell expression or VDJ data produced by 10X Genomics.",
            doi="10.1038/ncomms14049",
        )

        # Set up class objects to hold parsed data
        n = dict()

        # Call submodule functions
        n["count"] = parse_count_html(self)
        if n["count"] > 0:
            log.info(f"Found {n['count']} Cell Ranger count reports")

        n["vdj"] = parse_vdj_html(self)
        if n["vdj"] > 0:
            log.info(f"Found {n['vdj']} Cell Ranger VDJ reports")

        # Exit if we didn't find anything
        if sum(n.values()) == 0:
            raise ModuleNoSamplesFound
