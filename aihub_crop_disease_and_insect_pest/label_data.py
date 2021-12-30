def get_label_name(dataset_type, disease, crop, area):
    if dataset_type == "greenhouse_crop_disease":
        disease_list = greenhouse_crop_disease
        crop_list = greenhouse_crop_disease_crops
        labels_dict = greenhouse_crop_disease_labels_dict
    elif dataset_type == "fruit_burn_disease":
        disease_list = fruit_burn_disease
        crop_list = fruit_burn_disease_crops
        labels_dict = fruit_burn_disease_labels_dict
    elif dataset_type == "field_crop_disease":
        disease_list = field_crop_disease
        crop_list = field_crop_disease_crops
        labels_dict = field_crop_disease_labels_dict
    elif dataset_type == "field_crop_pest":
        disease_list = field_crop_pest
        labels_dict = field_crop_pest_labels_dict
        try:
            key = disease_list[disease]
        except:
            return None
        if key not in labels_dict:
            return None
        return labels_dict[key]

    try:
        key = "{}_{}_{}".format(disease_list[disease], crop_list[crop], plant_areas[area])
    except:
        return None
    if key not in labels_dict:
        return None
    return labels_dict[key]


def get_label_name_by_id(dataset_type, cate_id):
    if dataset_type == "greenhouse_crop_disease":
        labels = greenhouse_crop_disease_labels
    elif dataset_type == "fruit_burn_disease":
        labels = fruit_burn_disease_labels
    elif dataset_type == "field_crop_disease":
        labels = field_crop_disease_labels
    elif dataset_type == "field_crop_pest":
        labels = field_crop_pest_labels

    return labels[cate_id - 1]


greenhouse_crop_disease_labels = [
    '정상_가지_잎',
    '정상_가지_줄기',
    '정상_고추_잎',
    '정상_단호박_잎',
    '정상_딸기_잎',
    '정상_딸기_열매',
    '정상_딸기_꽃',
    '정상_딸기_줄기',
    '정상_상추_잎',
    '정상_수박_잎',
    '정상_애호박_잎',
    '정상_오이_잎',
    '정상_쥬키니호박_잎',
    '정상_참외_잎',
    '정상_토마토_잎',
    '정상_포도_잎',
    '가지잎곰팡이병_가지_잎',
    '가지흰가루병_가지_잎',
    '가지흰가루병_가지_줄기',
    '고추마일드모틀바이러스_고추_잎',
    '고추점무늬병_고추_잎',
    '단호박점무늬병_단호박_잎',
    '단호박흰가루병_단호박_잎',
    '딸기잿빛곰팡이병_딸기_잎',
    '딸기흰가루병_딸기_잎',
    '딸기잿빛곰팡이병_딸기_열매',
    '딸기흰가루병_딸기_열매',
    '딸기잿빛곰팡이병_딸기_꽃',
    '딸기흰가루병_딸기_꽃',
    '딸기잿빛곰팡이병_딸기_줄기',
    '딸기흰가루병_딸기_줄기',
    '상추균핵병_상추_잎',
    '상추노균병_상추_잎',
    '수박탄저병_수박_잎',
    '수박흰가루병_수박_잎',
    '애호박점무늬병_애호박_잎',
    '오이모자이크바이러스_오이_잎',
    '오이녹반모자이크바이러스_쥬키니호박_잎',
    '참외노균병_참외_잎',
    '참외흰가루병_참외_잎',
    '토마토잎곰팡이병_토마토_잎',
    '토마토황화잎말이바이러스_토마토_잎',
    '포도노균병_포도_잎',
]
greenhouse_crop_disease_labels_dict = {l: i + 1 for i, l in enumerate(greenhouse_crop_disease_labels)}
greenhouse_crop_disease = [
    '정상',
    '가지잎곰팡이병',
    '가지흰가루병',
    '고추마일드모틀바이러스',
    '고추점무늬병',
    '단호박점무늬병',
    '단호박흰가루병',
    '딸기잿빛곰팡이병',
    '딸기흰가루병',
    '상추균핵병',
    '상추노균병',
    '수박탄저병',
    '수박흰가루병',
    '애호박점무늬병',
    '오이녹반모자이크바이러스',
    '오이모자이크바이러스',
    '참외노균병',
    '참외흰가루병',
    '토마토잎곰팡이병',
    '토마토황화잎말이바이러스',
    '포도노균병',
]
greenhouse_crop_disease_crops = [
    '작물없음',
    '가지',
    '고추',
    '단호박',
    '딸기',
    '상추',
    '수박',
    '애호박',
    '오이',
    '쥬키니호박',
    '참외',
    '토마토',
    '포도'
]

plant_areas = [
    '구분없음',
    '열매',
    '꽃',
    '잎',
    '가지',
    '줄기',
    '뿌리',
    '해충'
]
fruit_burn_disease_labels = [
    '정상_배_열매',
    '정상_배_잎',
    '정상_배_가지',
    '정상_배_줄기',
    '정상_사과_열매',
    '정상_사과_잎',
    '정상_사과_줄기',
    '정상_사과_가지',
    '배검은별무늬병_배_열매',
    '배검은별무늬병_배_잎',
    '배과수화상병_배_잎',
    '배과수화상병_배_가지',
    '배과수화상병_배_줄기',
    '사과탄저병_사과_열매',
    '사과과수화상병_사과_잎',
    '사과갈색무늬병_사과_잎',
    '사과점무늬낙엽병_사과_잎',
    '사과과수화상병_사과_줄기',
    '사과부란병_사과_줄기',
    '사과과수화상병_사과_가지',
    '사과부란병_사과_가지',
]
fruit_burn_disease_labels_dict = {l: i + 1 for i, l in enumerate(fruit_burn_disease_labels)}
fruit_burn_disease = [
    '정상',
    '배검은별무늬병',
    '배과수화상병',
    '사과갈색무늬병',
    '사과과수화상병',
    '사과부란병',
    '사과점무늬낙엽병',
    '사과탄저병',
]
fruit_burn_disease_crops = [
    '작물없음',
    '배',
    '사과',
]

field_crop_disease_labels = [
    '정상_고추_열매',
    '정상_고추_잎',
    '정상_무_잎',
    '정상_배추_잎',
    '정상_애호박_잎',
    '정상_양배추_잎',
    '정상_오이_잎',
    '정상_토마토_잎',
    '정상_콩_잎',
    '정상_파_잎',
    '정상_호박_잎',
    '고추탄저병_고추_열매',
    '고추흰가루병_고추_잎',
    '무검은무늬병_무_잎',
    '무노균병_무_잎',
    '배추검음썩음병_배추_잎',
    '배추노균병_배추_잎',
    '애호박노균병_애호박_잎',
    '애호박흰가루병_애호박_잎',
    '양배추균핵병_양배추_잎',
    '양배추무름병_양배추_잎',
    '오이노균병_오이_잎',
    '오이흰가루병_오이_잎',
    '토마토잎마름병_토마토_잎',
    '콩불마름병_콩_잎',
    '콩점무늬병_콩_잎',
    '파검은무늬병_파_잎',
    '파노균병_파_잎',
    '파녹병_파_잎',
    '호박노균병_호박_잎',
    '호박흰가루병_호박_잎',
]
field_crop_disease_labels_dict = {l: i + 1 for i, l in enumerate(field_crop_disease_labels)}
field_crop_disease = [
    '정상',
    '고추탄저병',
    '고추흰가루병',
    '무검은무늬병',
    '무노균병',
    '배추검음썩음병',
    '배추노균병',
    '애호박노균병',
    '애호박흰가루병',
    '양배추균핵병',
    '양배추무름병',
    '오이노균병',
    '오이흰가루병',
    '콩불마름병',
    '콩점무늬병',
    '토마토잎마름병',
    '파검은무늬병',
    '파노균병',
    '파녹병',
    '호박노균병',
    '호박흰가루병'
]

field_crop_disease_crops = [
    '작물없음',
    '고추',
    '무',
    '배추',
    '애호박',
    '양배추',
    '오이',
    '토마토',
    '콩',
    '파',
    '호박',
]
field_crop_pest_labels = [
    '검거세미밤나방',
    '꽃노랑총채벌레',
    '담배가루이',
    '담배거세미나방',
    '담배나방',
    '도둑나방',
    '먹노린재',
    '목화바둑명나방',
    '무잎벌',
    '배추좀나방',
    '배추흰나비',
    '벼룩잎벌레',
    '복숭아혹진딧물',
    '비단노린재',
    '썩덩나무노린재',
    # '알락수염노린재',
    '열대거세미나방',
    '큰28점박이무당벌레',
    '톱다리개미허리노린재',
    '파밤나방',
]
field_crop_pest_labels_dict = {l: i + 1 for i, l in enumerate(field_crop_pest_labels)}
field_crop_pest = [
    '정상',
    '검거세미밤나방',
    '꽃노랑총채벌레',
    '담배가루이',
    '담배거세미나방',
    '담배나방',
    '도둑나방',
    '먹노린재',
    '목화바둑명나방',
    '무잎벌',
    '배추좀나방',
    '배추흰나비',
    '벼룩잎벌레',
    '복숭아진딧물',
    '복숭아혹진딧물',
    '비단노린재',
    '썩덩나무노린재',
    '알락수염노린재',
    '열대거세미나방',
    '큰28점박이무당벌레',
    '톱다리개미허리노린재',
    '파밤나방',
]
field_crop_pest_crops = [
    '작물없음',
    '감자',
    '고추',
    '들깨',
    '무',
    '배추',
    '벼',
    '양배추',
    '오이',
    '옥수수',
    '콩',
    '토마토',
    '파',
]
