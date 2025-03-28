import os
import cv2
import pytest
from typing import List
import numpy as np
from manga_translator.textline_merge import dispatch as dispatch_merge
from manga_translator.utils import (
    TextBlock,
    Quadrilateral,
    visualize_textblocks,
)

BBOX_IMAGE_FOLDER = 'test/testdata/bboxes'
os.makedirs(BBOX_IMAGE_FOLDER, exist_ok=True)

def save_regions_to_image(path: str, regions: TextBlock, width: int, height: int):
    img = np.zeros((height, width, 3))
    cv2.imwrite(path, visualize_textblocks(img, regions))

def find_region_containing_line(line, regions):
    """
    Finds region index which contains the `line`.
    """
    for i, region in enumerate(regions):
        for rline in region.lines:
            if (line == rline).all():
                return i
    raise ValueError('regions do not contain line')

async def generate_combinations(lines: List[List[List[int]]], width: int, height: int):
    """
    Returns the line combination and regions generated by the textline merge.
    """
    regions = await dispatch_merge([Quadrilateral(np.array(line), '', 1) for line in lines], width, height)
    generated_combinations = []
    for region in regions:
        combination = []
        for rline in region.lines:
            for i, line in enumerate(lines):
                if (line == rline).all():
                    combination.append(i)
                    break
        combination.sort()
        generated_combinations.append(combination)
    return generated_combinations, regions

async def run_test(lines: List, expected_combinations: List, width: int, height: int, path = None):
    generated_combinations, regions = await generate_combinations(lines, width, height)

    # Save as image
    path = os.path.join(BBOX_IMAGE_FOLDER, path or 'bboxes.png')
    save_regions_to_image(path, regions, width, height)

    expected_as_tuples = set(tuple(combination) for combination in expected_combinations)
    generated_as_tuples = set(tuple(combination) for combination in generated_combinations)

    assert expected_as_tuples == generated_as_tuples, f"image saved under {path}"

        # # Search for all associated regions
        # associated_regions = []
        # similar_expected_combination = None
        # for combination in expected_combinations:
        #     if generated_combination[0] in combination:
        #         similar_expected_combination = combination
        #         break
        # assert similar_expected_combination is not None
        # for j in similar_expected_combination:
        #     ri = find_region_containing_line(lines[j], regions)
        #     if ri and ri not in associated_regions:
        #         associated_regions.append(ri)

        # raise Exception(f'Regions: {associated_regions} should be merged - Image saved under {path}')


@pytest.mark.asyncio
async def test_merge_image1(): # demo/image/original3.jpg
    width, height = 2590, 4096
    lines = [
        [[   0, 3280], [ 237, 3234], [ 394, 4069], [ 149, 4096]],
        [[2400, 3210], [2493, 3210], [2498, 4061], [2405, 4061]],
        [[2306, 3208], [2410, 3208], [2416, 3992], [2312, 3992]],
        [[2226, 3208], [2328, 3208], [2328, 4050], [2226, 4050]],
        [[2149, 3205], [2242, 3205], [2237, 4005], [2144, 4005]],
        [[2160, 2298], [2245, 2298], [2250, 3069], [2165, 3069]],
        [[2082, 2296], [2176, 2296], [2176, 3032], [2082, 3032]],
        [[2008, 2293], [2109, 2293], [2109, 2680], [2008, 2680]],
        [[ 162, 1733], [ 256, 1733], [ 256, 2141], [ 162, 2141]],
        [[ 242, 1733], [ 336, 1733], [ 336, 2144], [ 242, 2144]],
        [[2269, 1349], [2368, 1349], [2373, 1960], [2274, 1960]],
        [[2186, 1352], [2288, 1352], [2288, 1760], [2186, 1760]],
        [[2373, 1357], [2442, 1357], [2442, 2077], [2373, 2077]],
        [[ 536, 1349], [ 613, 1349], [ 613, 1997], [ 536, 1997]],
        [[ 594, 1344], [ 680, 1344], [ 696, 2072], [ 610, 2072]],
        [[1037,  485], [1282,  469], [1349, 1418], [1104, 1434]],
        [[ 234,  528], [ 312,  528], [ 312, 1176], [ 234, 1176]],
        [[ 138,  509], [ 256,  509], [ 256,  706], [ 138,  706]],
        [[2418,  384], [2504,  384], [2509, 1234], [2424, 1234]],
        [[2344,  381], [2429,  381], [2434,  965], [2349,  965]],
        [[2269,  376], [2370,  376], [2370,  818], [2269,  818]],
        [[ 197,   42], [2405,   37], [2405,  362], [ 197,  368]],
    ]
    expected_combinations = [[0], [1, 2, 3, 4], [5, 6, 7], [8, 9], [10, 11, 12], [13, 14], [15], [16, 17], [18, 19, 20], [21]]
    await run_test(lines, expected_combinations, width, height, '1.png')

@pytest.mark.asyncio
async def test_merge_image1_upscaled(): # demo/image/original3.jpg upscaled x2
    width, height = 5180, 8192
    # detector has picked up less textlines
    lines = [
        [[   5, 6698], [ 506, 6602], [ 794, 8133], [ 293, 8192]],
        [[4800, 6421], [4986, 6421], [4997, 8122], [4810, 8122]],
        [[4618, 6416], [4821, 6416], [4837, 7984], [4634, 7984]],
        [[4453, 6416], [4656, 6416], [4656, 8096], [4453, 8096]],
        [[4298, 6410], [4485, 6410], [4474, 8010], [4288, 8010]],
        [[4309, 4592], [4496, 4592], [4512, 6144], [4325, 6144]],
        [[4165, 4592], [4352, 4592], [4352, 6064], [4165, 6064]],
        [[4016, 4586], [4218, 4586], [4218, 5360], [4016, 5360]],
        [[ 330, 3472], [ 517, 3472], [ 517, 4288], [ 330, 4288]],
        [[ 485, 3466], [ 672, 3466], [ 672, 4293], [ 485, 4293]],
        [[4544, 2704], [4730, 2704], [4741, 3909], [4554, 3909]],
        [[4373, 2704], [4576, 2704], [4576, 3520], [4373, 3520]],
        [[4746, 2714], [4885, 2714], [4885, 4149], [4746, 4149]],
        [[1072, 2709], [1226, 2709], [1226, 4000], [1072, 4000]],
        [[1189, 2693], [1360, 2693], [1392, 4138], [1221, 4138]],
        [[ 469, 1050], [ 624, 1050], [ 624, 2352], [ 469, 2352]],
        [[ 277, 1018], [ 512, 1018], [ 512, 1413], [ 277, 1413]],
        [[4837,  768], [5008,  768], [5018, 2469], [4848, 2469]],
        [[4688,  762], [4858,  762], [4869, 1930], [4698, 1930]],
        [[4538,  757], [4730,  757], [4741, 1632], [4549, 1632]],
        [[ 474,   80], [4805,   80], [4805,  730], [ 474,  730]],
    ]
    expected_combinations = [[0], [1, 2, 3, 4], [5, 6, 7], [8, 9], [10, 11, 12], [13, 14], [15, 16], [17, 18, 19], [20]]
    await run_test(lines, expected_combinations, width, height, '1_upscaled.png')

@pytest.mark.asyncio
async def test_merge_image2():
    width, height = 1317, 1637
    lines = [
        [[ 555, 1327], [ 609, 1311], [ 641, 1423], [ 588, 1439]],
        [[ 588, 1297], [ 637, 1285], [ 665, 1396], [ 616, 1407]],
        [[ 229, 1033], [ 280, 1019], [ 303, 1107], [ 252, 1121]],
        [[ 265,  996], [ 311,  992], [ 318, 1078], [ 272, 1082]],
        [[  65,  953], [ 111,  950], [ 149, 1434], [ 102, 1437]],
        [[ 119,  947], [ 169,  944], [ 219, 1579], [ 169, 1582]],
        [[1218,  894], [1271,  899], [1234, 1251], [1180, 1245]],
        [[1156,  886], [1219,  893], [1158, 1441], [1095, 1435]],
        [[1243,  201], [1305,  213], [1190,  800], [1128,  788]],
        [[1181,  189], [1246,  201], [1185,  557], [1120,  545]],
        [[1130,  180], [1190,  191], [1090,  686], [1030,  674]],
        [[1075,  169], [1133,  181], [1025,  718], [ 966,  706]],
        [[1009,  154], [1076,  166], [1033,  422], [ 966,  410]],
        [[ 960,  142], [1023,  155], [ 910,  694], [ 847,  682]],
        [[ 742,   31], [ 804,   38], [ 759,  489], [ 698,  482]],
        [[ 688,   26], [ 744,   33], [ 669,  720], [ 612,  714]],
        [[ 624,   14], [ 686,   21], [ 629,  573], [ 568,  566]],
        [[ 566,    9], [ 629,   15], [ 585,  473], [ 522,  466]],
    ]
    expected_combinations = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9, 10, 11, 12, 13], [14, 15, 16, 17]]
    await run_test(lines, expected_combinations, width, height, '2.png')

@pytest.mark.asyncio
async def test_merge_image3():
    width, height = 1920, 1360
    lines = [
        [[  46,  467], [ 103,  462], [ 158, 1122], [ 101, 1127]],
        [[1651,  322], [1703,  318], [1716,  512], [1663,  516]],
        [[1702,  317], [1756,  315], [1778,  748], [1725,  751]],
        [[1758,  313], [1810,  311], [1825,  638], [1773,  641]],
        [[ 752,  261], [ 800,  265], [ 775,  525], [ 727,  521]],
        [[ 471,  228], [ 528,  221], [ 627,  935], [ 570,  942]],
        [[1243,  128], [1631,  101], [1688,  888], [1301,  916]],
        [[ 540,  215], [ 597,  207], [ 681,  812], [ 623,  820]],
        [[ 592,  181], [ 662,  166], [ 715,  412], [ 645,  427]],
        [[ 852,  107], [ 903,  101], [ 962,  633], [ 911,  640]],
        [[ 223,   97], [ 288,   97], [ 297,  936], [ 232,  936]],
        [[1816,   45], [1885,   50], [1862,  345], [1793,  340]],
        [[1745,   42], [1815,   43], [1808,  346], [1738,  345]],
    ]
    expected_combinations = [[0], [10], [1, 2, 3], [11, 12], [5, 7, 8], [4], [9], [6]]
    await run_test(lines, expected_combinations, width, height, '3.png')

@pytest.mark.asyncio
async def test_merge_image4(): # Issue #215
    width, height = 800, 1280
    lines = [
        [[ 467, 1074], [ 614, 1073], [ 614, 1110], [ 467, 1111]],
        [[ 484, 1041], [ 600, 1041], [ 600, 1081], [ 484, 1081]],
        [[ 358,  952], [ 515,  952], [ 515,  989], [ 358,  989]],
        [[ 351,  920], [ 513,  920], [ 513,  956], [ 351,  956]],
        [[ 378,  886], [ 484,  886], [ 484,  926], [ 378,  926]],
        [[ 388,  852], [ 477,  856], [ 475,  895], [ 386,  891]],
        [[ 164,  629], [ 298,  628], [ 298,  668], [ 164,  669]],
        [[ 184,  594], [ 270,  594], [ 270,  640], [ 184,  640]],
        [[ 149,  563], [ 305,  562], [ 305,  605], [ 149,  605]],
        [[ 127,  532], [ 330,  532], [ 330,  571], [ 127,  571]],
        [[ 179,  497], [ 274,  495], [ 275,  541], [ 180,  543]],
    ]
    expected_combinations = [[0, 1], [2, 3, 4, 5], [6, 7, 8, 9, 10]]
    await run_test(lines, expected_combinations, width, height, '4.png')

@pytest.mark.asyncio
async def test_merge_image5(): # Issue #221
    width, height = 2750, 2750
    lines = [
        [[  10, 2698], [ 379, 2698], [ 379, 2744], [  10, 2744]],
        [[ 137, 2658], [ 250, 2658], [ 250, 2714], [ 137, 2714]],
        [[  19, 1457], [ 660, 1405], [ 689, 1754], [  48, 1806]],
        [[ 390,  637], [ 553,  637], [ 553,  674], [ 390,  674]],
        [[ 381,  599], [ 562,  599], [ 562,  653], [ 381,  653]],
        [[ 377,  572], [ 567,  572], [ 567,  621], [ 377,  621]],
        [[ 368,  538], [ 571,  535], [ 571,  594], [ 368,  597]],
        [[ 397,  512], [ 540,  508], [ 542,  563], [ 399,  567]],
        [[ 408,  490], [ 529,  481], [ 533,  529], [ 411,  538]],
        [[ 282,  415], [ 368,  415], [ 368,  454], [ 282,  454]],
        [[ 222,  381], [ 433,  379], [ 433,  427], [ 222,  429]],
        [[ 216,  352], [ 436,  352], [ 436,  399], [ 216,  399]],
        [[ 250,  327], [ 395,  327], [ 395,  365], [ 250,  365]],
        [[ 288,  300], [ 354,  300], [ 354,  333], [ 288,  333]],
    ]
    expected_combinations = [[0], [1], [2], [3, 4, 5, 6, 7, 8], [9, 10, 11, 12, 13]]
    await run_test(lines, expected_combinations, width, height, '5.png')

@pytest.mark.asyncio
async def test_merge_image6():
    width, height = 1441, 2048
    lines = [
        [[1153, 1496], [1255, 1496], [1255, 1528], [1153, 1528]],
        [[1159, 1460], [1251, 1460], [1251, 1496], [1159, 1496]],
        [[1137, 1430], [1273, 1430], [1273, 1458], [1137, 1458]],
        [[1157, 1394], [1255, 1394], [1255, 1424], [1157, 1424]],
        [[1149, 1362], [1265, 1362], [1265, 1390], [1149, 1390]],
        [[1123, 1330], [1283, 1330], [1283, 1358], [1123, 1358]],
        [[226, 885], [305, 891], [302, 929], [223, 923]],
        [[193, 856], [333, 860], [331, 894], [192, 890]],
        [[191, 822], [327, 826], [325, 860], [190, 856]],
        [[472, 818], [638, 818], [638, 844], [472, 844]],
        [[204, 792], [320, 792], [320, 826], [204, 826]],
        [[470, 782], [630, 782], [630, 810], [470, 810]],
        [[474, 752], [622, 752], [622, 774], [474, 774]],
        [[464, 716], [632, 716], [632, 744], [464, 744]],
        [[460, 682], [642, 682], [642, 710], [460, 710]],
        [[506, 650], [592, 650], [592, 680], [506, 680]],
        [[812, 425], [899, 430], [897, 461], [810, 456]],
        [[809, 396], [919, 396], [919, 424], [809, 424]],
        [[162, 398], [254, 398], [254, 420], [162, 420]],
        [[821, 364], [901, 364], [901, 392], [821, 392]],
        [[114, 364], [306, 364], [306, 390], [114, 390]],
        [[143, 324], [273, 328], [272, 356], [142, 352]],
        [[142, 298], [272, 298], [272, 320], [142, 320]],
        [[552, 282], [642, 282], [642, 318], [552, 318]],
        [[128, 262], [288, 262], [288, 288], [128, 288]],
        [[536, 254], [660, 254], [660, 282], [536, 282]],
        [[1037,  238], [1203,  238], [1203,  264], [1037,  264]],
        [[534, 220], [660, 220], [660, 248], [534, 248]],
        [[1067,  204], [1181,  204], [1181,  232], [1067,  232]],
        [[530, 186], [668, 186], [668, 214], [530, 214]],
        [[1055,  172], [1187,  172], [1187,  200], [1055,  200]],
        [[538, 154], [660, 154], [660, 182], [538, 182]],
    ]
    expected_combinations = [[0, 1, 2, 3, 4, 5], [6, 7, 8, 10], [9, 11, 12, 13, 14, 15], [16, 17, 19], [18, 20, 21, 22, 24], [23, 25, 27, 29, 31], [26, 28, 30]]
    await run_test(lines, expected_combinations, width, height, '6.png')

@pytest.mark.asyncio
async def test_merge_image7():
    width, height = 1700, 2400
    lines = [
        [[ 287, 2123], [ 343, 2123], [ 343, 2332], [ 287, 2332]],
        [[ 225, 2120], [ 292, 2120], [ 292, 2287], [ 225, 2287]],
        [[ 120, 1859], [ 171, 1859], [ 175, 2075], [ 123, 2075]],
        [[ 210, 1857], [ 270, 1854], [ 276, 1953], [ 217, 1956]],
        [[ 171, 1857], [ 223, 1857], [ 220, 2076], [ 168, 2076]],
        [[ 318, 1734], [ 375, 1734], [ 375, 1931], [ 318, 1931]],
        [[ 368, 1731], [ 429, 1731], [ 429, 1882], [ 368, 1882]],
        [[1217,  937], [1273,  939], [1270, 1120], [1214, 1118]],
        [[1259,  937], [1318,  934], [1325, 1035], [1265, 1039]],
        [[1437,  785], [1492,  785], [1492, 1068], [1437, 1068]],
        [[1487,  784], [1542,  782], [1548, 1025], [1493, 1026]],
        [[1381,  782], [1435,  782], [1435, 1026], [1381, 1026]],
        [[142, 429], [184, 429], [181, 607], [139, 607]],
        [[103, 431], [143, 431], [143, 640], [103, 640]],
        [[192, 209], [260, 207], [267, 492], [198, 493]],
        [[431, 201], [473, 201], [473, 356], [431, 356]],
        [[384, 200], [435, 200], [435, 360], [384, 360]],
        [[346, 201], [393, 201], [393, 393], [346, 393]],
        [[1559,  118], [1600,  118], [1600,  415], [1559,  415]],
        [[1468,  117], [1509,  117], [1509,  448], [1468,  448]],
        [[1510,  115], [1551,  115], [1554,  415], [1514,  415]],
        [[575, 107], [620, 107], [620, 318], [575, 318]],
        [[535, 107], [581, 107], [581, 318], [535, 318]],
        [[614, 106], [659, 106], [659, 318], [614, 318]],
        [[496, 106], [543, 106], [543, 253], [496, 253]],
    ]
    expected_combinations = [[0, 1], [2, 3, 4], [5, 6], [7, 8], [9, 10, 11], [12, 13], [14], [15, 16, 17], [21, 22, 23, 24], [18, 19, 20]]
    await run_test(lines, expected_combinations, width, height, '7.png')

@pytest.mark.asyncio
async def test_merge_image8():
    width, height = 1115, 1600
    lines = [
        [[429, 167], [470, 167], [470, 247], [429, 247]],
        [[406, 175], [428, 175], [428, 306], [406, 306]],
        [[ 993,   97], [1017,   97], [1017,  158], [ 993,  158]],
        [[ 636, 1469], [ 659, 1469], [ 659, 1531], [ 636, 1531]],
        [[431, 519], [454, 519], [454, 584], [431, 584]],
        [[161, 483], [187, 483], [187, 570], [161, 570]],
        [[529, 438], [551, 438], [551, 528], [529, 528]],
        [[ 234,  998], [ 261,  998], [ 261, 1125], [ 234, 1125]],
        [[728, 480], [750, 480], [750, 589], [728, 589]],
        [[562, 438], [589, 438], [589, 572], [562, 572]],
        [[ 267, 1384], [ 294, 1384], [ 294, 1519], [ 267, 1519]],
        [[978, 417], [999, 417], [999, 522], [978, 522]],
        [[568,  78], [595,  78], [595, 234], [568, 234]],
        [[ 170, 1388], [ 192, 1388], [ 192, 1517], [ 170, 1517]],
        [[458, 520], [479, 520], [479, 644], [458, 644]],
        [[912, 720], [943, 720], [943, 905], [912, 905]],
        [[537,  80], [559,  80], [559, 212], [537, 212]],
        [[904, 130], [926, 130], [926, 264], [904, 264]],
        [[137, 484], [158, 484], [158, 631], [137, 631]],
        [[ 203, 1386], [ 225, 1386], [ 225, 1541], [ 203, 1541]],
        [[839, 131], [860, 131], [860, 284], [839, 284]],
        [[701, 480], [721, 480], [721, 633], [701, 633]],
        [[ 270, 1002], [ 297, 1002], [ 297, 1209], [ 270, 1209]],
        [[ 236, 1384], [ 259, 1385], [ 258, 1563], [ 234, 1562]],
        [[871, 131], [893, 131], [893, 308], [871, 308]],
    ]
    expected_combinations = [[0, 1], [2], [3], [4, 14], [5, 18], [6, 9], [7, 22], [8, 21], [10, 13, 19, 23], [11], [12, 16], [15], [17, 20, 24]]
    await run_test(lines, expected_combinations, width, height, '8.png')

@pytest.mark.asyncio
async def test_merge_image9():
    width, height = 1158, 1637
    lines = [
        [[ 527,  957], [ 646,  933], [ 685, 1129], [ 565, 1153]],
        [[  0,  89], [112,  73], [142, 311], [ 14, 327]],
        [[ 866,  824], [ 967,  803], [1010, 1006], [ 909, 1027]],
        [[ 213,  791], [ 327,  771], [ 373, 1028], [ 258, 1048]],
        [[ 969, 1483], [1008, 1475], [1033, 1609], [ 996, 1616]],
        [[484,  20], [553,  20], [556, 334], [488, 334]],
        [[550,  20], [617,  22], [605, 369], [539, 367]],
        [[1018,   20], [1080,   21], [1075,  426], [1013,  425]],
        [[1080,    9], [1148,    9], [1152,  464], [1083,  464]],
    ]
    expected_combinations = [[0], [2], [3], [1], [4], [5, 6], [7, 8]]
    await run_test(lines, expected_combinations, width, height, '9.png')

@pytest.mark.asyncio
async def test_merge_image10():
    width, height = 3035, 4299
    lines = [
        [[298, 420], [357, 420], [357, 567], [298, 567]],
        [[2628, 1612], [2674, 1612], [2674, 1788], [2628, 1788]],
        [[ 982, 3250], [1287, 3240], [1289, 3316], [ 984, 3326]],
        [[1339, 1948], [1398, 1948], [1398, 2229], [1339, 2229]],
        [[1410, 1948], [1469, 1948], [1469, 2233], [1410, 2233]],
        [[1520,  231], [1578,  231], [1578,  525], [1520,  525]],
        [[2632, 1772], [2674, 1772], [2674, 2003], [2632, 2003]],
        [[1595,  235], [1641,  235], [1641,  508], [1595,  508]],
        [[2569, 1608], [2624, 1608], [2624, 1948], [2569, 1948]],
        [[348, 424], [403, 424], [403, 814], [348, 814]],
        [[1444,  231], [1503,  231], [1503,  697], [1444,  697]],
        [[2665, 1609], [2720, 1608], [2729, 2052], [2674, 2053]],
        [[1645, 3187], [1704, 3186], [1713, 3832], [1654, 3833]],
        [[1708, 3195], [1750, 3195], [1750, 3795], [1708, 3795]],
    ]
    # print((await generate_combinations(lines, width, height))[0])
    expected_combinations = [[0, 9], [1, 6, 8, 11], [2], [3, 4], [5, 7, 10], [12, 13]]
    await run_test(lines, expected_combinations, width, height, '10.png')
