#pip install google-cloud-video-intelligence
from google.cloud import videointelligence

def detect_ppe(video_path):
    """Detects people and PPE in a video."""

    client = videointelligence.VideoIntelligenceServiceClient()

    # Configure the request
    config = videointelligence.types.PersonalProtectionEquipmentConfig(
        include_bounding_boxes=True,
        include_coverages=True,
        include_confidences=True,
        required_equipment_types=[
            videointelligence.PersonalProtectionEquipmentConfig.EquipmentType.FACE_COVER,
            videointelligence.PersonalProtectionEquipmentConfig.EquipmentType.HEAD_COVER,
            videointelligence.PersonalProtectionEquipmentConfig.EquipmentType.HAND_COVER,
        ],
    )

    context = videointelligence.types.VideoContext(personal_protection_equipment_detection_config=config)

    # Start the asynchronous request
    operation = client.annotate_video(
        request={
            "features": [videointelligence.Feature.PERSONAL_PROTECTION_EQUIPMENT_DETECTION],
            "input_uri": video_path,
            "video_context": context,
        }
    )

    print("\nProcessing video for PPE detection.")
    result = operation.result(timeout=300)

    print("\nFinished processing.\n")

    # Retrieve the first result, because a single video was processed.
    ppe_annotation = result.annotation_results[0].personal_protection_equipment_annotations

    for annotation in ppe_annotation:
        print(f"Entity description: {annotation.entity.description}")
        print(f"Entity id: {annotation.entity.entity_id}")

        for track in annotation.tracks:
            print(f"Track confidence: {track.confidence}")

            for segment in track.segments:
                start_time = (
                    segment.segment.start_time_offset.seconds
                    + segment.segment.start_time_offset.microseconds / 1e6
                )
                end_time = (
                    segment.segment.end_time_offset.seconds
                    + segment.segment.end_time_offset.microseconds / 1e6
                )
                print(f"Segment: {start_time}s to {end_time}s")

            for timestamped_object in track.timestamped_objects:
                print(f"Timestamp: {timestamped_object.time_offset.seconds + timestamped_object.time_offset.microseconds / 1e6}s")

                for bounding_box in timestamped_object.normalized_bounding_box:
                    print(f"Bounding box position:")
                    print(f"\tleft  : {bounding_box.left}")
                    print(f"\ttop   : {bounding_box.top}")
                    print(f"\tright : {bounding_box.right}")
                    print(f"\tbottom: {bounding_box.bottom}")

                for attribute in timestamped_object.attributes:
                    print(f"Attribute: {attribute.name}")
                    print(f"\tValue: {attribute.value}")
                    print(f"\tConfidence: {attribute.confidence}")

                for landmark in timestamped_object.landmarks:
                    print(f"Landmark: {landmark.name}")
                    print(f"\tConfidence: {landmark.confidence}")
                    print(f"\t3D position: {landmark.position}")

def main():
    video_path = "gs://bucket-name/path-to-video.mp4"
    detect_ppe(video_path)

if __name__ == "__main__":
    main()
