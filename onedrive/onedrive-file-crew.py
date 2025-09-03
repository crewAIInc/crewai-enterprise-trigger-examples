from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class OneDriveFileTrigger:
    """OneDriveFileTrigger crew for OneDrive file operations"""

    @agent
    def onedrive_file_analyzer(self) -> Agent:
        return Agent(
            role="OneDrive File Payload Parser and Analyzer",
            goal="Parse OneDrive file payload data to extract file details (name, type, permissions, metadata) and analyze file operations for business insights",
            backstory="You're an expert at parsing Microsoft Graph API payload structures and OneDrive file data formats. You excel at navigating complex JSON structures to extract file information including name, size, createdDateTime, lastModifiedDateTime, permissions, and sharing settings. You understand different file types, folder structures, and OneDrive file operations like creation, updates, deletions, and sharing changes.",
            verbose=True
        )

    @agent
    def onedrive_file_summarizer(self) -> Agent:
        return Agent(
            role="OneDrive File Operation Summarization Specialist",
            goal="Create clear, concise summaries that prominently display file name, type, and operation, then capture essential file details and business context",
            backstory="You're a skilled communicator who specializes in distilling complex file operation information into clear, actionable summaries. You excel at organizing information with file name and operation type prominently displayed at the top, followed by comprehensive file analysis. You understand that file name, type, and operation are the most critical pieces of information for quick file identification and security assessment.",
            verbose=True
        )

    @task
    def onedrive_file_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a OneDrive file operation with the following structure:
            - result.id: File ID
            - result.name: File name
            - result.size: File size in bytes
            - result.createdDateTime: File creation timestamp
            - result.lastModifiedDateTime: Last modification timestamp
            - result.webUrl: Web URL for file access
            - result.parentReference: Parent folder information
            - result.file: File-specific properties (if it's a file)
            - result.folder: Folder-specific properties (if it's a folder)
            - result.createdBy: User who created the file
            - result.lastModifiedBy: User who last modified the file
            - result.permissions: Sharing and access permissions

            IMPORTANT: Extract the following information from the payload structure:

            1. File Basic Information:
               - File ID (result.id)
               - File name (result.name)
               - File size (result.size)
               - File or folder type determination

            2. Timestamps and Metadata:
               - Creation time (result.createdDateTime)
               - Last modified time (result.lastModifiedDateTime)
               - Version information if available

            3. Location and Context:
               - Parent folder information (result.parentReference)
               - Web URL (result.webUrl)
               - File path context

            4. User Activity:
               - Created by user (result.createdBy)
               - Last modified by user (result.lastModifiedBy)
               - User collaboration patterns

            5. Access and Security:
               - Permissions and sharing (result.permissions)
               - Access levels and security implications
               - External sharing status

            6. Analyze the file operation for:
               - Type of operation (new file, update, delete, share)
               - File type and business relevance
               - Security and compliance implications
               - Collaboration and sharing context
               - Business impact and importance
            """,
            expected_output="""
            A structured analysis containing:
            - File Information:
              * File ID: [OneDrive file ID]
              * Name: [file name]
              * Type: [file or folder type]
              * Size: [file size in bytes]
            - Timeline:
              * Created: [creation timestamp]
              * Modified: [last modification timestamp]
              * Operation: [type of file operation detected]
            - Location:
              * Parent: [parent folder information]
              * Web URL: [file access URL]
              * Path Context: [organizational location]
            - User Activity:
              * Created By: [user who created the file]
              * Modified By: [user who last modified]
              * Collaboration: [user interaction patterns]
            - Access Control:
              * Permissions: [sharing and access settings]
              * Security Level: [access restriction analysis]
              * External Sharing: [external access status]
            - Analysis:
              * Operation type and context
              * File business relevance
              * Security implications
              * Collaboration impact
              * Organizational importance
            """,
            agent=self.onedrive_file_analyzer
        )

    @task
    def onedrive_file_summarization_task(self) -> Task:
        return Task(
            description="""
            Based on the file operation analysis from the parsed OneDrive payload, create a comprehensive summary that includes:
            - The file name extracted from the "name" field in the payload
            - The operation type and timing from the analysis
            - Key file details and metadata from the analysis
            - User activity and collaboration context
            - Important security or sharing considerations
            - Assessment of business impact and relevance

            IMPORTANT: Ensure the file name (from "name" field) and operation type
            are displayed prominently at the top of your summary. These are critical pieces of
            information that must be clearly visible for quick file operation identification.
            """,
            expected_output="""
            A well-structured OneDrive file operation summary in markdown format containing:
            - **File ID**: OneDrive file ID (from result.id in payload)
            - **File Name**: File name (extracted from "name" field)
            - **Type**: File or folder type
            - **Operation**: Type of file operation (new, update, delete, share)
            - **Size**: File size in bytes (if applicable)
            - **Created**: File creation timestamp and user
            - **Modified**: Last modification timestamp and user
            - **Location**: Parent folder and file path context
            - **Web URL**: Direct access link to the file
            - **Permissions**: Sharing and access permissions
            - **Security**: Access level and external sharing status
            - **Summary**: Concise overview of the file operation
            - **User Activity**: Collaboration and modification patterns
            - **Business Context**: Organizational relevance and impact
            - **Security Notes**: Any compliance or access considerations
            - **Recommended Actions**: Next steps or follow-up items

            Ensure the File Name and Operation fields are prominently displayed at the top and
            formatted as clean markdown without code blocks.
            """,
            agent=self.onedrive_file_summarizer,
            output_file='onedrive_file_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the OneDriveFileTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = OneDriveFileTrigger().crew()
    crewai_trigger_payload = "PUT YOUR TRIGGER PAYLOAD HERE"
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
