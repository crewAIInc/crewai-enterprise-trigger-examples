from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class OutlookEventRemovalTrigger:
    """OutlookEventRemovalTrigger crew for calendar event deletion notifications"""

    @agent
    def event_removal_analyzer(self) -> Agent:
        return Agent(
            role="Outlook Event Removal Analyzer",
            goal="Parse Outlook event removal payload data to extract deletion details and analyze calendar disruption impact",
            backstory="You're an expert at parsing Outlook event removal notifications and understanding calendar management patterns. You excel at analyzing event deletion activities, understanding the impact on scheduled meetings, and assessing workflow disruption from calendar changes.",
            verbose=True
        )

    @agent
    def event_removal_summarizer(self) -> Agent:
        return Agent(
            role="Event Removal Summarization Specialist",
            goal="Create clear summaries of event removal notifications that highlight scheduling impact and follow-up needs",
            backstory="You're skilled at analyzing calendar event deletions and providing insights into meeting disruption, rescheduling needs, and team communication requirements based on event removal activities.",
            verbose=True
        )

    @task
    def event_removal_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains an Outlook event removal notification with the following structure:
            - result.@odata.etag: Entity tag for the deleted event
            - result.@odata.id: OData identifier for the user and deleted event
            - result.@odata.type: Microsoft Graph Event type
            - result.id: Event ID of the removed event

            IMPORTANT: Extract the following information:

            1. Removal Event Details:
               - Event ID that was removed
               - OData identifiers and references
               - User context (from @odata.id path)
               - Entity versioning information

            2. Impact Assessment:
               - Calendar event deletion confirmation
               - User whose calendar was affected
               - Potential meeting disruption
               - Follow-up communication needs

            3. Context Analysis:
               - Type of event removal (cancellation vs deletion)
               - User workflow impact
               - Team coordination requirements

            Note: This is a minimal removal notification, so detailed event information
            (title, attendees, time) is not available in the payload. Focus on the
            deletion event itself and its implications.
            """,
            expected_output="""
            A structured analysis containing:
            - Removal Event:
              * Event ID: [ID of removed event]
              * OData Type: [Microsoft Graph event type]
              * User Context: [Affected user from path]
              * Entity Tag: [Version/state information]
            - Deletion Details:
              * Removal Confirmed: [Event deletion status]
              * Calendar Affected: [User's calendar impacted]
              * Notification Type: [Event removal notification]
            - Impact Analysis:
              * Meeting Disruption: [Potential schedule impact]
              * Communication Needs: [Required follow-up]
              * Workflow Impact: [Calendar management effects]
              * Coordination Requirements: [Team notification needs]
            - Recommendations:
              * Investigate: [Check if meeting was cancelled or rescheduled]
              * Communicate: [Notify affected participants]
              * Follow-up: [Ensure alternative arrangements made]
            """,
            agent=self.event_removal_analyzer
        )

    @task
    def event_removal_summarization_task(self) -> Task:
        return Task(
            description="""
            Create a comprehensive summary of the event removal notification that includes scheduling impact,
            communication needs, and recommended actions for meeting coordination.
            """,
            expected_output="""
            An event removal summary in markdown format:
            - **Event ID**: ID of the removed event
            - **Removal Type**: Event deletion/cancellation notification
            - **Affected User**: User whose calendar was impacted
            - **OData Reference**: Microsoft Graph entity information
            - **Status**: Event removal confirmed
            - **Calendar Impact**: Schedule disruption assessment
            - **Meeting Status**: Cancelled/rescheduled determination needed
            - **Communication Needs**: Required participant notifications
            - **Workflow Impact**: Effect on daily schedule and commitments
            - **Recommended Actions**:
              - Verify if event was cancelled or rescheduled
              - Check for alternative meeting arrangements
              - Notify affected attendees if needed
              - Update related calendar dependencies
            - **Priority Level**: Urgency based on potential meeting importance
            - **Follow-up Required**: Next steps for meeting coordination
            """,
            agent=self.event_removal_summarizer,
            output_file='event_removal_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the OutlookEventRemovalTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = OutlookEventRemovalTrigger().crew()
    # Example payload from event-removed.json
    crewai_trigger_payload = """{
        "result": {
            "@odata.etag": "W/\\"XyZABCDEFGHIJKLMNOPQRSTUVWXYZ123456\\"",
            "@odata.id": "Users/ab12c345-6789-0def-ghij-klmnopqrstuv/Events/AQMkABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
            "@odata.type": "#Microsoft.Graph.Event",
            "id": "AQMkABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        }
    }"""
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
