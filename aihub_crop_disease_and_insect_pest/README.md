# image-preprocessing
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