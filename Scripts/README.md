## LaneRecognition Description
- CameraCalibration을 통한 직선 왜곡 보정
```
참고 [https://docs.opencv.org/3.4.3/dc/dbb/tutorial_py_calibration.html]
```
- 전처리 과정을 통해 왜곡된 직선을 직선 형태로 수정
- ROI를 바탕으로 차선 인식 Region 외의 Thresholding적용
- 원근 변환을 통해 전방 도로이미지를 변환. 
- Sliding Window Searching을 통해 곡선 차선의 인식오차 최소화
- 최종적으로 인식된 차선을 바탕으로 인식결과를 표시함.
- 실질적 주행을 위해서는 조명, 바닥면 상태를 고려할 수 있는 머신러닝 모델의 지원이 필요할 듯.
