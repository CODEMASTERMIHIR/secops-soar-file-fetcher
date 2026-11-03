from SiemplifyAction import SiemplifyAction

def main():
    siemplify = SiemplifyAction()
    
    # Extracts the dynamic path passed from the Playbook UI
    file_path = siemplify.extract_action_param("File Path", print_value=True)
    
    try:
        siemplify.add_attachment(file_path, description="Encrypted Vendor Archive")
        siemplify.end(f"Successfully attached the ZIP file from {file_path}", True)
    except Exception as e:
        siemplify.end(f"Failed to attach file: {str(e)}", False)

if __name__ == "__main__":
    main()
