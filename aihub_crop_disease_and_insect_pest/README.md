# image-preprocessing
0. 이미지 전처리
   - common/resize.py
      - resize: 이미지 사이즈 작게 줄이기(yolo로 학습 시키려고 width or height 최소 길이 700으로 지정)
      - orientation 정상으로 돌리기
      - 에러 이미지 삭제
1. 각 데이터셋별로 사용할 클래스 선정하기
   - stat_category.py : 해충 데이터셋만 라벨데이터 구조가 달라서 따로 카테고리 통계를 보기 위한 코드
   - stat_data.py : 데이터셋종류, 식물종류, 식물부위, 카테고리별로 통계 내는 코드
   - label_data.py : 데이터셋 별로 카테고리(클래스) 정보가 들어있는 코드
2. 각 데이터셋 coco 포멧으로 변경
   - convert_labels_to_coco.py: coco 포멧으로 변경하는 코드로 데이터셋_phase(train or val) 별로 실행해야 함.
   - check list
      - resize 됐으면 bbox도 비율에 맞게 변경
      - 실제 image_path 없을경우 처리
      - 메타데이터가 이상할 경우 무시하도록
      - category 확인, annotations, images 갯수 확인, anno, image 개별 아이템 확인
   - review
      - https://github.com/jireh-father/coco-viewer.git
      - 실행해서 확인
3. 전체 coco 합치기
   - merge_cocos.py
4. split train & val strategy
   - stat_cocos.py
   - coco/split_coco_train_val_strategy.py
   - review by coco-viewer
5. convert coco to yolo format
6. training yolo

## todo
seed
- 모든 train, val coco 정상여부 검토 시각 V
  - category 정보확인 V
  - 시각화 확인해보기 V
- 모든 train & val coco 데이터셋 merge
- merge한 coco 데이터셋 카테고리 통계내기
 - 정상 최대 갯수 지정
- merge한 coco에서 정상 최대 갯수 이하 랜덤으로 버리기
 - 안버린것도 가지고 있기
- split train * val
- yolo학습
 - yolo 데이터셋 변환
 - yolo 학습 세팅
 - 학습 및 평가

## checklist
0. check 
   - 노지 작물 해충 진단 이미지
    - 13 복숭아진딧물
    - 14 복숭아혹진딧물
    - 13번을 14번으로 모두 이동한게 맞는지 ? 맞음 빙고!
1. 각 데이터셋 coco로 변환
2. 각 coco 데이터셋 정상여부 확인

## 정상데이터 처리 고민
정상모두 모아서?
## train & val 어떻게 나눌지 고민
- 원래 나눠진데로?
- train과 val 따로 검토해보기


## 기타 데이터셋
```json

{
    "description": {
        "image": "V006_77_0_00_01_01_13_0_c03_20201209_0000_S01_3.jpg",
        "date": "2020/12/09",
        "worker": "",
        "height": 4032,
        "width": 2268,
        "task": 77,
        "type": 0,
        "region": null
    },
    "annotations": {
        "disease": 0,
        "crop": 1,
        "area": 1,
        "grow": 13,
        "risk": 0,
        "points": [
            {
                "xtl": 941,
                "ytl": 1245,
                "xbr": 1387,
                "ybr": 2753
            }
        ]
    }
}
```

## 노지 작물 해충 진단 이미지
- 13 복숭아진딧물
- 14 복숭아혹진딧물
- 13번을 14번으로 모두 이동
```json
{
    "description": {
        "image": "V006_78_3_19_01_03_12_1_2634r_20201027_27.jpeg",
        "date": "2020/10/27",
        "height": 3024,
        "width": 4032,
        "task": 78,
        "type": 3,
        "region": 7
    },
    "annotations": {
        "crop": 1,
        "area": 3,
        "risk": 1,
        "object": [
            {
                "id": 0,
                "class": 19,
                "grow": 12,
                "points": [
                    {
                        "xtl": 0,
                        "ytl": 617,
                        "xbr": 2676,
                        "ybr": 2238
                    }
                ]
            }
        ]
    }
}

```