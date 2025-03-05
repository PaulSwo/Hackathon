def update_image():
    # Capture the current camera frame
    frame = face_recognition.get_camera_frame()
    
    # Scan faces in the frame
    recognized_faces = face_recognition.scan_faces_in_frame(frame)

    # Clear previous danger message
    danger_label.config(text="")

    # Check each recognized face against the dangerous persons list
    for face in recognized_faces:
        # Assuming face contains 'id' (unique identifier for each face)
        face_id = face.get("id")
        
        # Search for the person in the dangerous persons list
        person = next((p for p in dangerous_persons if p["face_id"] == face_id), None)
        
        if person:
            # If the person is found in the dangerous list, display the danger warning
            danger_label.config(text=f"Dangerous person detected: {person['name']} (Level: {person['danger_level']})")
        else:
            # No dangerous person detected
            danger_label.config(text="No dangerous persons detected")
    
    # Convert frame to PhotoImage for displaying
    img = ImageTk.PhotoImage(image=Image.fromarray(frame))
    
    # Update the image label with the new frame
    image.photo_image = img
    image.config(image=image.photo_image)

    # Schedule the next update
    root.after(10, update_image)  # Update the image every 10 ms
