#!/usr/bin/env python3

import json
from os import path

import click
from core.rnd.rndgen import MarcianiMultiStream, MarcianiSingleStream
from core.utils import guiutils, logutils
from exp.analytical import analytical_solution
from exp.rnd import (
    extremes,
    jumpfind,
    kolmogorov_smirnov,
    modulus,
    mulcheck,
    mulfind,
    spectral,
)
from exp.simulation import performance_analysis, transient_analysis, validation

logger = logutils.get_logger(__name__)


@click.group(invoke_without_command=True, context_settings=dict(max_content_width=120))
@click.option("--debug/--no-debug", default=False, show_default=True, type=bool, help="Activate/Deactivate debug mode.")
@click.pass_context
@click.version_option(version="1.0.0")
def main(ctx, debug):
    print(guiutils.get_splash())
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
    else:
        logutils.set_log_level(logger, "DEBUG" if debug else "INFO")
        logger.debug("Debug Mode: {}".format("on" if debug else "off"))


@main.command(help="Find a modulus for bits.")
@click.option("--bits", default=modulus.DEFAULT_BITS, show_default=True, type=int, help="Number of bits.")
@click.option(
    "--outdir",
    default=modulus.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.pass_context
def find_modulus(ctx, bits, outdir):
    logger.info("Executing: {}".format(modulus.__file__))
    logger.info("Arguments: bits={} | outdir={}".format(bits, outdir))
    modulus.run(bits, outdir)
    logger.info("Completed: {}".format(modulus.__file__))


@main.command(help="Find FP, MC, FP/MC multipliers for modulus.")
@click.option("--modulus", default=mulfind.DEFAULT_MODULUS, show_default=True, type=int, help="Modulus.")
@click.option(
    "--outdir",
    default=mulfind.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.pass_context
def find_multipliers(ctx, modulus, outdir):
    logger.info("Executing: {}".format(mulfind.__file__))
    logger.info("Arguments: modulus={} | outdir={}".format(modulus, outdir))
    mulfind.run(modulus, outdir)
    logger.info("Completed: {}".format(mulfind.__file__))


@main.command(help="Find jumpers for modulus/multiplier/streams.")
@click.option("--modulus", default=jumpfind.DEFAULT_MODULUS, show_default=True, type=int, help="Modulus.")
@click.option("--multiplier", default=jumpfind.DEFAULT_MULTIPLIER, show_default=True, type=int, help="Multiplier.")
@click.option("--streams", default=jumpfind.DEFAULT_STREAMS, show_default=True, type=int, help="Streams.")
@click.option(
    "--outdir",
    default=jumpfind.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.pass_context
def find_jumpers(ctx, modulus, multiplier, streams, outdir):
    logger.info("Executing: {}".format(jumpfind.__file__))
    logger.info(
        "Arguments: modulus={} | multiplier={} | streams={} | outdir={}".format(modulus, multiplier, streams, outdir)
    )
    jumpfind.run(modulus, multiplier, streams, outdir)
    logger.info("Completed: {}".format(jumpfind.__file__))


@main.command(help="Check FP, MC, FP/MC constraints.")
@click.option("--modulus", default=mulcheck.DEFAULT_MODULUS, show_default=True, type=int, help="Modulus.")
@click.option("--multiplier", default=mulcheck.DEFAULT_MULTIPLIER, show_default=True, type=int, help="Multiplier.")
@click.option(
    "--outdir",
    default=mulcheck.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.pass_context
def check_multiplier(ctx, modulus, multiplier, outdir):
    logger.info("Executing: {}".format(mulcheck.__file__))
    logger.info("Arguments: modulus={} | multiplier={} | outdir={}".format(modulus, multiplier, outdir))
    mulcheck.run(modulus, multiplier, outdir)
    logger.info("Completed: {}".format(mulcheck.__file__))


@main.command(help="Test of Randomness: Spectral.")
@click.option("--modulus", default=spectral.DEFAULT_MODULUS, show_default=True, type=int, help="Modulus.")
@click.option("--multiplier", default=spectral.DEFAULT_MULTIPLIER, show_default=True, type=int, help="Multiplier.")
@click.option("--samsize", default=spectral.DEFAULT_SAMSIZE, show_default=True, type=int, help="Sample size.")
@click.option("--interval", default=spectral.DEFAULT_INTERVAL, show_default=True, type=tuple, help="Zoomed interval.")
@click.option(
    "--outdir",
    default=spectral.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.pass_context
def test_spectral(ctx, modulus, multiplier, samsize, interval, outdir):
    logger.info("Executing: {}".format(spectral.__file__))
    logger.info(
        "Arguments: modulus={} | multiplier={} | samsize={} | interval={} | outdir={}".format(
            modulus, multiplier, samsize, interval, outdir
        )
    )
    generator = MarcianiSingleStream(modulus=modulus, multiplier=multiplier)
    spectral.run(generator, samsize, interval, outdir)
    logger.info("Completed: {}".format(spectral.__file__))


@main.command(help="Test of Randomness: Extremes.")
@click.option("--modulus", default=extremes.DEFAULT_MODULUS, show_default=True, type=int, help="Modulus.")
@click.option("--multiplier", default=extremes.DEFAULT_MULTIPLIER, show_default=True, type=int, help="Multiplier.")
@click.option("--jumper", default=extremes.DEFAULT_JUMPER, show_default=True, type=int, help="Jumper.")
@click.option("--streams", default=extremes.DEFAULT_STREAMS, show_default=True, type=int, help="Streams.")
@click.option("--samsize", default=extremes.DEFAULT_SAMSIZE, show_default=True, type=int, help="Sample size.")
@click.option("--bins", default=extremes.DEFAULT_BINS, show_default=True, type=int, help="Bins.")
@click.option(
    "--confidence", default=extremes.DEFAULT_CONFIDENCE, show_default=True, type=float, help="Confidence level."
)
@click.option("--d", default=extremes.DEFAULT_D, show_default=True, type=int, help="Test parameter D.")
@click.option(
    "--outdir",
    default=extremes.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.pass_context
def test_extremes(ctx, modulus, multiplier, jumper, streams, samsize, bins, confidence, d, outdir):
    logger.info("Executing: {}".format(extremes.__file__))
    logger.info(
        "Arguments: modulus={} | multiplier={} | jumper={} | streams={} | samsize={} | bins={} | confidence={} | d={} | outdir={}".format(
            modulus, multiplier, jumper, streams, samsize, bins, confidence, d, outdir
        )
    )
    generator = MarcianiMultiStream(modulus=modulus, multiplier=multiplier, jumper=jumper, streams=streams)
    extremes.run(generator, samsize, bins, confidence, d, outdir)
    logger.info("Completed: {}".format(extremes.__file__))


@main.command(help="Test of Randomness: Kolmogorov-Smirnov.")
@click.option("--modulus", default=kolmogorov_smirnov.DEFAULT_MODULUS, show_default=True, type=int, help="Modulus.")
@click.option(
    "--multiplier", default=kolmogorov_smirnov.DEFAULT_MULTIPLIER, show_default=True, type=int, help="Multiplier."
)
@click.option("--jumper", default=kolmogorov_smirnov.DEFAULT_JUMPER, show_default=True, type=int, help="Jumper.")
@click.option("--streams", default=kolmogorov_smirnov.DEFAULT_STREAMS, show_default=True, type=int, help="Streams.")
@click.option(
    "--test",
    default=kolmogorov_smirnov.DEFAULT_TEST,
    show_default=True,
    type=click.Choice([kolmogorov_smirnov.SUPPORTED_TESTS], case_sensitive=False),
    help="Underlying test of randomness.",
)
@click.option(
    "--test-params",
    default=kolmogorov_smirnov.DEFAULT_TEST_PARAMS,
    show_default=True,
    type=click.STRING,
    help="Params for the underlying test of randomness.",
)
@click.option(
    "--outdir",
    default=kolmogorov_smirnov.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.pass_context
def test_kolmogorov_smirnov(ctx, modulus, multiplier, jumper, streams, test, test_params, outdir):
    logger.info("Executing: {}".format(kolmogorov_smirnov.__file__))
    logger.info(
        "Arguments: modulus={} | multiplier={} | jumper={} | streams={} | test={} | test_params={} | outdir={}".format(
            modulus, multiplier, jumper, streams, test, test_params, outdir
        )
    )
    generator = MarcianiMultiStream(modulus=modulus, multiplier=multiplier, jumper=jumper, streams=streams)
    kolmogorov_smirnov.run(generator, test, test_params, path.join(outdir, test))
    logger.info("Completed: {}".format(kolmogorov_smirnov.__file__))


@main.command(help="Simulate (Transient Analysis): Cloud-Cloudlet.")
@click.option(
    "--config",
    default=transient_analysis.DEFAULT_CONFIG_PATH,
    show_default=True,
    type=click.Path(exists=True),
    help="Configuration.",
)
@click.option(
    "--outdir",
    default=transient_analysis.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.option(
    "--parameters",
    default=transient_analysis.DEFAULT_PARAMETERS,
    show_default=True,
    type=str,
    help="Parameters (JSON), e.g. {'system': {'cloudlet': {'threshold': 20}}}.",
)
@click.pass_context
def simulate_transient(ctx, config, outdir, parameters):
    logger.info("Executing: {}".format(transient_analysis.__file__))
    logger.info("Arguments: config={} | outdir={} | parameters={}".format(config, outdir, parameters))
    transient_analysis.run(config, outdir, json.loads(str(parameters)))
    logger.info("Completed: {}".format(transient_analysis.__file__))


@main.command(help="Simulate (Performance Analysis): Cloud-Cloudlet.")
@click.option(
    "--config",
    default=performance_analysis.DEFAULT_CONFIG_PATH,
    show_default=True,
    type=click.Path(exists=True),
    help="Configuration.",
)
@click.option(
    "--outdir",
    default=performance_analysis.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.option(
    "--parameters",
    default=performance_analysis.DEFAULT_PARAMETERS,
    show_default=True,
    type=str,
    help='Parameters (JSON), e.g. \'{"system": {"cloudlet": {"threshold": 20}}}\'.',
)
@click.pass_context
def simulate_performance(ctx, config, outdir, parameters):
    logger.info("Executing: {}".format(performance_analysis.__file__))
    logger.info("Arguments: config={} | outdir={} | parameters={}".format(config, outdir, parameters))
    performance_analysis.run(config, outdir, json.loads(str(parameters)))
    logger.info("Completed: {}".format(performance_analysis.__file__))


@main.command(help="Solve with Markov Chain: Cloud-Cloudlet.")
@click.option(
    "--config",
    default=analytical_solution.DEFAULT_CONFIG_PATH,
    show_default=True,
    type=click.Path(exists=True),
    help="Configuration.",
)
@click.option(
    "--outdir",
    default=analytical_solution.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.option(
    "--parameters",
    default=analytical_solution.DEFAULT_PARAMETERS,
    show_default=True,
    type=str,
    help='Parameters (JSON), e.g. \'{"system": {"cloudlet": {"threshold": 20}}}\'.',
)
@click.pass_context
def solve_cloud_cloudlet(ctx, config, outdir, parameters):
    logger.info("Executing: {}".format(analytical_solution.__file__))
    logger.info("Arguments: config={} | outdir={} | parameters={}".format(config, outdir, parameters))
    analytical_solution.run(config, outdir, json.loads(str(parameters)))
    logger.info("Completed: {}".format(analytical_solution.__file__))


@main.command(help="Validate: Cloud-Cloudlet.")
@click.option(
    "--analytical-result",
    default=validation.DEFAULT_ANALYTICAL_RESULT_PATH,
    show_default=True,
    type=click.Path(exists=True),
    help="Analytical result.",
)
@click.option(
    "--simulation-result",
    default=validation.DEFAULT_SIMULATION_RESULT_PATH,
    show_default=True,
    type=click.Path(exists=True),
    help="Simulation result.",
)
@click.option(
    "--outdir",
    default=validation.DEFAULT_OUTDIR,
    show_default=True,
    type=click.Path(exists=False),
    help="Output directory.",
)
@click.pass_context
def validate_cloud_cloudlet(ctx, analytical_result, simulation_result, outdir):
    logger.info("Executing: {}".format(validation.__file__))
    logger.info(
        "Arguments: analytical_result={} | simulation_result={} | outdir={}".format(
            analytical_result, simulation_result, outdir
        )
    )
    validation.run(analytical_result, simulation_result, outdir)
    logger.info("Completed: {}".format(validation.__file__))


if __name__ == "__main__":
    main(obj={})
