from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Response
from services.detection import DetectionService

detector = DetectionService()

router=APIRouter()

@router.post('/detect')
async def detect_objects(
    file: UploadFile = File(...),
    confidence_threshold: float = Query(0.25, ge=0.0, le=1.0)
):
    try:
        contents = await file.read()
        annotated_image_bytes = detector.detect_and_annotate(
            image_bytes=contents,
            conf_threshold=confidence_threshold
        )
        return Response(
            content=annotated_image_bytes,
            media_type="image/jpeg",
            headers={
                "Content-Disposition": f"inline; filename=detected_{file.filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")