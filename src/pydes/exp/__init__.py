"""
Keep in mind the following table:

╔════════════╦════════════════════════════════════════════════╗
║            ║                      BITS                      ║
║            ╠═════╦═══════╦════════════╦═════════════════════╣
║            ║ 8   ║ 16    ║ 32         ║ 64                  ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MODULUS    ║ 127 ║ 32479 ║ 2147483647 ║ 9223372036854775783 ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MULTIPLIER ║ 14  ║ 16374 ║ 48271      ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ STREAMS    ║ 64  ║ 128   ║ 256        ║ 512                 ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ JUMPER     ║ 14  ║ 32748 ║ 22925      ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ CHECKV     ║     ║       ║ 399268537  ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ CHECKI     ║     ║       ║ 10000      ║                     ║
╚════════════╩═════╩═══════╩════════════╩═════════════════════╝
"""

# import os

# EXP_DIR = os.path.dirname(os.path.abspath(__file__)) + '/resources'
# PLT_EXT = 'svg'
# RES_EXT = 'txt'
