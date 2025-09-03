from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class GoogleDriveFileDeletionTrigger:
    """GoogleDriveFileDeletionTrigger crew for file deletion/change notifications"""

    @agent
    def file_deletion_analyzer(self) -> Agent:
        return Agent(
            role="Google Drive File Deletion Analyzer",
            goal="Parse Google Drive file deletion/change payload data to extract deletion details and analyze file removal impact",
            backstory="You're an expert at parsing Google Drive change notifications and understanding file deletion events. You excel at analyzing file removal patterns, understanding the impact of deletions on team workflows, and assessing data loss risks from file deletion activities.",
            verbose=True
        )

    @agent
    def file_deletion_summarizer(self) -> Agent:
        return Agent(
            role="File Deletion Event Summarization Specialist",
            goal="Create clear summaries of file deletion events that highlight security implications and workflow impact",
            backstory="You're skilled at analyzing file deletion data and providing insights into data security, workflow disruption, and potential recovery needs based on file removal events.",
            verbose=True
        )

    @task
    def file_deletion_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a Google Drive change notification for a file deletion with the following structure:
            - result.kind: "drive#change"
            - result.removed: true (indicates file was deleted)
            - result.fileId: ID of the deleted file
            - result.time: Timestamp of the deletion
            - result.type: "file"
            - result.changeType: "file"

            IMPORTANT: Extract the following information:

            1. Deletion Event Details:
               - Change type and confirmation of removal
               - File ID of deleted file
               - Deletion timestamp
               - Change notification type

            2. Impact Assessment:
               - File deletion confirmation
               - Timeline of deletion event
               - Potential workflow disruption
               - Data loss implications

            3. Security Analysis:
               - Unauthorized deletion risk
               - Data protection concerns
               - Recovery requirements
               - Audit trail needs

            Note: This is a change notification, so detailed file information (name, type, etc.)
            is not available in the payload. Focus on the deletion event itself.
            """,
            expected_output="""
            A structured analysis containing:
            - Deletion Event:
              * Change Type: [drive#change]
              * Status: [File removed/deleted]
              * File ID: [ID of deleted file]
              * Timestamp: [Deletion time]
            - Event Details:
              * Change Kind: [Type of change notification]
              * Removal Confirmed: [Boolean confirmation]
              * Change Category: [File change type]
            - Impact Analysis:
              * Data Loss: [File deletion confirmed]
              * Workflow Impact: [Potential disruption]
              * Recovery Needs: [File restoration requirements]
              * Security Implications: [Data protection concerns]
            - Recommendations:
              * Investigation: [Need to identify deleted file]
              * Recovery Actions: [Restore from trash if needed]
              * Security Review: [Check for unauthorized access]
            """,
            agent=self.file_deletion_analyzer
        )

    @task
    def file_deletion_summarization_task(self) -> Task:
        return Task(
            description="""
            Create a comprehensive summary of the file deletion event that includes security implications,
            workflow impact, and recommended actions for file recovery and investigation.
            """,
            expected_output="""
            A file deletion event summary in markdown format:
            - **Change Type**: Drive change notification type
            - **Event**: File deletion confirmed
            - **File ID**: ID of the deleted file
            - **Deletion Time**: When the file was removed
            - **Status**: Removal confirmation status
            - **Data Loss Impact**: Assessment of information lost
            - **Workflow Disruption**: Potential impact on team operations
            - **Security Concerns**: Unauthorized access or accidental deletion risks
            - **Recovery Options**: Available restoration methods
            - **Recommended Actions**:
              - Investigate deleted file details
              - Check Google Drive trash for recovery
              - Review access logs for security
              - Notify affected team members
            - **Priority Level**: Urgency of response based on file importance
            """,
            agent=self.file_deletion_summarizer,
            output_file='file_deletion_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GoogleDriveFileDeletionTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = GoogleDriveFileDeletionTrigger().crew()
    # Example payload from deleted-file.json
    crewai_trigger_payload = """{
        "result": {
            "kind": "drive#change",
            "removed": true,
            "fileId": "XXXXXXXXXXXX",
            "time": "2023-05-08T09:29:25.032Z",
            "type": "file",
            "changeType": "file"
        }
    }"""
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
