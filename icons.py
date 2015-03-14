# AvsP - an AviSynth editor
# 
# Copyright 2007 Peter Jang <http://avisynth.nl/users/qwerpoi>
#           2010-2012 the AvsPmod authors <https://github.com/avspmod/avspmod>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA, or visit
#  http://www.gnu.org/copyleft/gpl.html .

# icons - icons embedded in a Python script
# 
# Dependencies:
#     Python (tested on v2.6 and v2.7)
#     wxPython (tested on v2.8 Unicode and v2.9)

from wx.lib.embeddedimage import PyEmbeddedImage

AvsP_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAgZJ"
    "REFUWIXtl6FywjAch38pmN2RoXbH3bgZqlD0AYKo6gwvgmMPALzAHK+A2QPAISqK2dwUCgy3"
    "qblRu2WiJLTQJG2BMbG/IrmQ39fv0iQlxCrhkmVdNP0vAJTTOvn3Fy86IbFK5CgA/v3FgyBA"
    "pVLR/jEMQ/i+j+dNHwAwXQMIV+ATm+cBIfFFKMJrtRrCMMwcHi8BgomdCUICiHDbtg/C421d"
    "eBEIQqySDG+1WgeB++3xeKwNzwuRWAOUUu2ky+XSGCzKuwOmC/O41LdABeL7Pj6qfTSqUXv1"
    "Zpi90gDul+ATm6sslIFoxbbbbc55+tsXBxrd7vq7BogsFhIb0Xw+Vw7cbDZwXReDxTAKr0cw"
    "jbo+QFpQ7C0SYGtBOQ+lFIyxRN9j0wzh3en5DrZinQUA6HQ6GCyGGL0BjeudCW1pLCQATBYA"
    "wHEc+Xu2hQCKW0g9jH7TwgFAUQvdejELyuM4j4XVZ9RXxEIqgLCgg3AcB67rAq8zjLZ7QREL"
    "SgMCghCiBGGMIfCupAkgvwXtjYhYJWICYYyh1+tJCJOF/cp0JTOBUEolBJDBQl6ALCAC4mY2"
    "VFqYro8EMIGIQ2tkOiVjdwRyiu8CsaCCIAAQHduDZh/ey26MfPonkrignORaHjciNrHuuzkc"
    "OJGB/RJGvAe+A0gJPxvAPgigvqafFSBLXfzT7B/gBzi2CON/wMBrAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
play_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAH5J"
    "REFUWIXt1EESwCAIQ1GQ3v/GHbvqXiBpuoAD+N+MivsKU86S1gcwgN8DwnyH+ZYBvoCkroAB"
    "Kb0BJKT1CBEQyC/oQKDfsAKh7IEMhLqITiDyTXgxD79tuwRwEqYAMmEooBKGADrhFgARLgGQ"
    "4RSAET4CMMPvyDfhAAYgBzzIPiRzQVyedwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
pause_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlw"
    "SFlzAAAN1wAADdcBQiibeAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoA"
    "AACCSURBVFiF7dexCYAwEIXh/8TaMRzAMZxGHM4xrMUJrF3g2YYQSLpYvMAVCY/LB2kuIYme"
    "a+h6uwF/AIwtoYiYgSU5eiUdWWYFpuTolHRXm0uqFrABSuoqZK4ss7X07v4EBhhggAEGGGCA"
    "AQY0DaXAATzJ/i1kdrKhtKVx+GtmQG/AB4GqXmFNBqwqAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
external_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlw"
    "SFlzAAAN1wAADdcBQiibeAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoA"
    "AAFiSURBVFiF7Za9SgNBFIXPmZn8WEgsrC21V7DwDUyTJoWVb2AbLO1EfA/tRFAQSxGLWEkK"
    "KwtrESxEUZLZY5EsjovGEJMdkD1w2d2ZO3u+3QtzhwAMAAfADu5tMBZGNRNzAOYBHEh6xZgy"
    "4y6clAqAAuD/AZCslGxpj+RI757GH6CklqU9JVmLAZBq3dFdk1yKBQBBi5a27ejqUQAGqoE4"
    "sbTbsQAAwJDcddYdkpyJAdCXsGForkgupEMEsIzPDhiGHUTaKcsAKsF1Fv2OeAbgLbApG5p2"
    "1ptg+PhAsdlV95IANKkPHCZDk4XoStqKvRPSAVhB/iV4pNjsqXfhANzgbyeiTngiIlnNmH2R"
    "oE6ipCHpHsi/GR0lStZS8zwBJGnHyzclvYQTLgfzZwibXv74u8lpA9x5+Yak258SplmCcy+/"
    "Osx8WgAiue/l65KefkueeAkkvQNojZofeycsAAqA+AAf/cVxOJ6qaHcAAAAASUVORK5CYII=")

#----------------------------------------------------------------------
next_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAHZJ"
    "REFUWIXt10sKACEMA9BU739k0RsM/aQoTLrtIg9sC5qNiZs1rqYLIIAAHsCE7Uq/DOhGuJ+g"
    "CxGagQ5EeAjZiNQWMBHpNWQhSneAgXj/EH3VwrZKvwRghKcBrPAUgBkeBrDDQ4COcDegKxwA"
    "TP8CAQT4PeAAzMIsUQFAh3wAAAAASUVORK5CYII=")

#----------------------------------------------------------------------
skip_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAH1J"
    "REFUWIXt10sKwDAIBNAxuf+RU7PqrhQ/IylUtwbmEaIQkTFxssbR9AY0oAEWwIRopn+XXuvx"
    "nOkGWIgwoBLhegMVCPcjZCNCU8BEhMeQhUjtAQbi+4vorRZUMv0UgBEeBrDCQwBmuBvADncB"
    "KsLNgKpwAJD+FzSgAb8HbDPFMErXwWvCAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
spin_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAMElEQVR42mNkoBAwDm8D/hNj"
    "ASEDCLqSGAPwqiPWAJxq6eICisKAolggCowawMAAAGI5BxGNrXGkAAAAAElFTkSuQmCC")

#----------------------------------------------------------------------
checked_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAWElEQVR42s2RQQoAIAgE82c+"
    "3Z8ZHYwsgxUh2kOHckbYqBVD4xARzYLMTE5gF0jW+acCjeZRgXUECeamDU4J7O2AM4IWwWgH"
    "eoMzJWoEV77xdwEKW5ygkg43FHEROvSJLgAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
unchecked_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAMUlEQVR42mNkoBAwgogDBw78"
    "J1Wjg4MDI4oBMAFiALL6UQNGDRhuBhCrGQZQDKAEAABsPGgR8pSNpgAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
smile_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAwNJ"
    "REFUOI1lk11Mm3UUxn//f8sKLLQbhQrd+ArQroOaZWMGGMwLlyyZgPFKXUx2Iy6LF7pdeqHR"
    "zOiWmPkRRW8k3rgY9YJ4sRiMqN0cc+qW0c6NlQJV6Nv3pYwBsgFve7xo3eb2JM/NyTnP8+Tk"
    "HKW0gweRTpkynTjP1MQvrK7mqNraRiDURV39FvVgr7pfwDQs+WPkRVwqga/CS1mZl7V1zV+p"
    "ea7EZjFuejn8ymnqG+4J3RVIJsYkHT3EtlAdG+trQBcDCmwNt4W1BZvfLk/zzbe/c7D/C3a3"
    "tysAZ97ZkEysh117w1BWw+3VHCWuyryFEyhzIFmLzifClJZ6GBx4nsmJpDQ01iqUdnBpuE/E"
    "elZEXpd3T/UKIPv37xCR0yLypfT1PSaAnHyzV2T5hAx9/py8/EKnKO1Ap2eT4q9YBK8X8BD5"
    "aQaAkZE4sAEo5scfbuRro3/Dxk0EGrbiLl1n4saEOG/NXaBmswdUEZDl668O8cmn2zlwYDfg"
    "AhTR2NsMDY1y+EgHkGWTuxi/v5prYxHUheFj0taSQldvAXwFevILJAvoQhIHsAxYzMVMhiMJ"
    "zFvFOO2sk9U7WUrQJBImtv0PgUCQexsUYAUoIhq7jtdl43I4yOZyOIs2oN2+TtJGBrCZSc3R"
    "2zNYcMwB6wUCaPqeGiAzs8Tyis18ZoFgqAtdWd3B+OQca1PzdO9poqPLR3//h4XIJQUqnjn4"
    "Dk/va6a1rY7r8QyWZRJs2ZM/pMH398n2xjV27dyGfsTP0WNnOHsuTVd3M5KDyM/j9Oxt5I3j"
    "T3L5/AyR0TjWzRWOn/peKaUdpI2MfPZeK93trbQEa/EE/CxOLxI5l0KJpqOtjs2Vbn69aHDp"
    "yixj0RivnTxLlb9C3T3l+HhcPjrRzo5wLcGmJnwVbtzuUtZtTcq4w2RyibFrSaanZnn1rTM0"
    "BwPqoWeyzEUZ+OAIU+PfUeUrp7zch21rUsY8hrlAKPw4Lx39mEqf5+Fnuh+WuSRXo6P8efUi"
    "IkL40U6CoZ3/G/wP/wJ3xTm0DZwlTwAAAABJRU5ErkJggg==")
    
#----------------------------------------------------------------------
question_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAACI0lEQVQ4jYWTwUsbQRTGfzOx"
    "SWZN06R4CcKeikQLpUJdmlrwppfmouip4KVQaKEI/SN66lGhIF57K7156m1FTSCUSkrQRLAQ"
    "4mVziDXo7Ganh26KyGo/eAwPvvfm+96bEcTjMfAamIryn8An4Pt1oogpfm5Z1seZmZkHhUIh"
    "C9DpdHrVarXZ7/ffA+5VciKmwYfZ2dlnY2NjOUCGYSiVUiqfz989OTm5B3y5SpbXip8AxVwu"
    "l9Vao7XG93183yefz2eBYsS5EQeO45wvLCyYbrf7L1zXNfPz88ZxnHPg4DYLT8fHx6dGR0fv"
    "NBoNXNdlMBgwPT1NvV6n3W777Xb7G/D1JgurlUplTwgRHB8f02q16PV6nJ6e4nleUKlU9oDV"
    "22YAsH54eNgFKBaLzM3NsbW1xf7+fhdYv83/VbRWVlZMs9k029vbZnl52QCtOOJITP5mqGxt"
    "bQ0hBEqpodp3wAYQxDVzgM/A0dLSkimXy6bT6ZidnR1TLpfN4uKiAY4ijjMsGm7hpWVZG7Zt"
    "PyqVSoUgCJBSMjk5ied51Go1tNZMTEzcD8PQvry8fOH7vgf8GD7leqlUKkopZTKZRClFMpnk"
    "7OwMgEwmg9aai4sLfN9nMBiEu7u7DeDhCGABdjqdllJKUqkUSilSqRTZbBZjDEEQkEgkEEIg"
    "pcQYIwEbsAR/f95b4BXQB35H0Qd0pDAdXZSJTgvYBNZFNHk7ZiP/QwD8+gOTQ9W5+jdpxQAA"
    "AABJRU5ErkJggg==")
    
#----------------------------------------------------------------------
ok_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAGXRFWHRTb2Z0d2FyZQBBZG9i"
    "ZSBJbWFnZVJlYWR5ccllPAAAAWVJREFUeNpi/P//PwNdgVsnw38QJkuzYxvD/3c/JoIxiE2y"
    "5idfmv/P2sQAxk+/NoJdwkKs5sV5zQzbj9QyMLAyMDACxb7/f4eqyB1omjsWvzkBNd/+XPR/"
    "1h6G/zOBePZehv+XPsX/d4J4wRiu6MqnOCCGS0DEW4GKPyb8n30Q6OwDQM2HQJoTUDWDbD37"
    "we//7GNABUcZ/p967//foZkBjEFskPgsoPgcIH36gz+qZiBggfuHmYHhH1Dqwq2NDLVpNmBJ"
    "EJuBCehnIFZTsWOomLaRYV8VgwlQ6izMAJB+Y5c2hjOlqboMj59cZvj3j4EBlrYYgbJMQM2y"
    "MroMXbMvM+xF0wwCQHsZnt/by7DlheCrNAd7WYYfPz4x/AfZCpRhBsaRiIQsw4Q5t7FqRgcg"
    "l/xf+Zz7/9wbDGAMYrug+ZkQMHYFalj9khuMXUnUDDfEExgznp3kaYYbQqxmRkqzM0CAAQBW"
    "bMG1YQFlxwAAAABJRU5ErkJggg==")

#----------------------------------------------------------------------
rectangle_icon = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAABXElEQVR42sXSv0vDQBQH8O9d"
    "ErUVp/ojCAoiiDjU/hAHlzq5WXBRu1pBEAc3J/EPcHIRWpFODv4Bzro4CEXQWRBc1FYpUps0"
    "lzTnpeqU10UFH2S6y4f3fe8YflnsT4F6sybfnCdwppGXfekjFh1FxIiyECA8IU9ut1CxbqDz"
    "HhIQXgOT/YtYmtoLA5ZoyEJ5GU2/Co0ZJOC2bJi9SeTTxxRgyWI5B0c+K6CL7qBlwYymsZYu"
    "EIATdJCDi4qaQWdgKJJCfqYYBhoBcJWDp1XBuYogw+N2PQsD3Smsz3YADi9VB7wKXTPAuDr8"
    "OpUK81sMwrUwGEliY65IRzg4X1VDfGnPoP1z8MlP4DvCcF8Cm5kjogPxLvfPVmCLGjROb8FR"
    "EUZicWwvEFtourbcPc2i8voAQ6ffgS3qiI9nsJMthYGgru8v5N2jekg6sQUVw/MFEmPzmDCn"
    "aeAn9f/AByV0jxHGo4HSAAAAAElFTkSuQmCC")
    
#----------------------------------------------------------------------
dragdrop_cursor = PyEmbeddedImage(
    "iVBORw0KGgoAAAANSUhEUgAAAA4AAAAYCAYAAADKx8xXAAAAhElEQVR42q3TgQ6AIAgE0OP/"
    "P9qspcM8hNtya6z0jSAyAK1fBnHZC6HiB/YFM5PwhM+NgBeo4A1WMYUVHMIMH+EJpzDCWY0s"
    "0Q7vw9VvyianNBBsViX43UxxVIMEZ60++g4v+155NA76bvvIMi7PyNs1mhHJXzHOZRnDxv2a"
    "EaUYdTWLF10UqgXtrhCoAAAAAElFTkSuQmCC")