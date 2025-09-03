from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class GoogleDriveFileTrigger:
    """GoogleDriveFileTrigger crew"""

    @agent
    def drive_file_analyzer(self) -> Agent:
        return Agent(
            role="Google Drive File Payload Parser and Analyzer",
            goal="Parse Google Drive file payload data to extract file details (name, type, permissions, metadata) and analyze file operations for insights",
            backstory="You're an expert at parsing Google Drive API payload structures and file data formats. You excel at navigating complex JSON structures to extract file information including name, mimeType, size, creation/modification dates, permissions, and sharing settings. You understand different file types, folder structures, and Drive file operations like creation, updates, and deletions.",
            verbose=True
        )

    @agent
    def drive_file_summarizer(self) -> Agent:
        return Agent(
            role="Drive File Operation Summarization Specialist",
            goal="Create clear, concise summaries that prominently display file name, type, and operation, then capture essential file details and context",
            backstory="You're a skilled communicator who specializes in distilling complex file operation information into clear, actionable summaries. You excel at organizing information with file name and operation type prominently displayed at the top, followed by comprehensive file analysis. You understand that file name, type, and operation are the most critical pieces of information for quick file identification.",
            verbose=True
        )

    @task
    def drive_file_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a Google Drive file operation with the following structure:
            - result.id: File ID
            - result.name: File name
            - result.mimeType: File MIME type
            - result.kind: Resource type (drive#file)
            - result.createdTime: File creation timestamp
            - result.modifiedTime: Last modification timestamp
            - result.size: File size in bytes (if applicable)
            - result.parents[]: Array of parent folder IDs
            - result.owners[]: Array of file owners
            - result.permissions[]: Array of sharing permissions

            IMPORTANT: Extract the following information from the payload structure:

            1. File Basic Information:
               - File ID (result.id)
               - File name (result.name)
               - File type/MIME type (result.mimeType)
               - File size (result.size if available)

            2. Timestamps and Metadata:
               - Creation time (result.createdTime)
               - Last modified time (result.modifiedTime)
               - Version information if available

            3. Location and Organization:
               - Parent folder IDs (result.parents)
               - File path context
               - Folder structure implications

            4. Ownership and Permissions:
               - File owners (result.owners)
               - Sharing permissions (result.permissions)
               - Access level analysis

            5. Analyze the file operation for:
               - Type of operation (new file, update, deletion)
               - File type and potential use case
               - Security and sharing implications
               - Collaboration context
               - Organizational impact
            """,
            expected_output="""
            A structured analysis containing:
            - File Information:
              * File ID: [Google Drive file ID]
              * Name: [file name]
              * Type: [MIME type and human-readable format]
              * Size: [file size if available]
            - Timeline:
              * Created: [creation timestamp]
              * Modified: [last modification timestamp]
              * Operation: [type of file operation detected]
            - Location:
              * Parent Folders: [parent folder IDs and context]
              * File Path: [organizational context]
            - Access Control:
              * Owners: [file owner information]
              * Permissions: [sharing and access permissions]
              * Visibility: [access level assessment]
            - Analysis:
              * Operation type and context
              * File purpose and use case
              * Security implications
              * Collaboration impact
              * Organizational relevance
            """,
            agent=self.drive_file_analyzer
        )

    @task
    def drive_file_summarization_task(self) -> Task:
        return Task(
            description="""
            Based on the file operation analysis from the parsed Google Drive payload, create a comprehensive summary that includes:
            - The file name extracted from the "name" field in the payload
            - The file type and format extracted from the "mimeType" field
            - The operation type and timing from the analysis
            - Key file details and metadata from the analysis
            - Any important security or sharing considerations
            - Assessment of file importance and organizational impact

            IMPORTANT: Ensure the file name (from "name" field) and operation type
            are displayed prominently at the top of your summary. These are critical pieces of
            information that must be clearly visible for quick file operation identification.
            """,
            expected_output="""
            A well-structured file operation summary in markdown format containing:
            - **File ID**: Google Drive file ID (from result.id in payload)
            - **File Name**: File name (extracted from "name" field)
            - **File Type**: MIME type and format (extracted from "mimeType" field)
            - **Operation**: Type of file operation (new, update, delete)
            - **Size**: File size (if available)
            - **Created**: File creation timestamp
            - **Modified**: Last modification timestamp
            - **Location**: Parent folder context and file path
            - **Owners**: File owner information
            - **Permissions**: Sharing and access permissions
            - **Summary**: Concise overview of the file operation
            - **Key Details**: Important information and context
            - **Security Notes**: Any access or sharing considerations
            - **Impact**: Assessment of organizational relevance

            Ensure the File Name and Operation fields are prominently displayed at the top and
            formatted as clean markdown without code blocks.
            """,
            agent=self.drive_file_summarizer,
            output_file='drive_file_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GoogleDriveFileTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = GoogleDriveFileTrigger().crew()
    crewai_trigger_payload = "PUT YOUR TRIGGER PAYLOAD HERE"
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
