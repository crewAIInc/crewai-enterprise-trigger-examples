from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class GoogleCalendarWorkingLocationTrigger:
    """GoogleCalendarWorkingLocationTrigger crew for working location events"""

    @agent
    def working_location_analyzer(self) -> Agent:
        return Agent(
            role="Google Calendar Working Location Event Analyzer",
            goal="Parse Google Calendar working location payload data to extract work location details, dates, and analyze remote work patterns",
            backstory="You're an expert at parsing Google Calendar working location events and understanding remote work patterns. You excel at extracting working location properties, understanding different location types (homeOffice, office, custom), and analyzing work-from-home schedules and hybrid work arrangements.",
            verbose=True
        )

    @agent
    def working_location_summarizer(self) -> Agent:
        return Agent(
            role="Working Location Event Summarization Specialist",
            goal="Create clear summaries of working location events that highlight location type, dates, and work arrangement insights",
            backstory="You're skilled at analyzing working location data and providing insights into remote work patterns, hybrid schedules, and team collaboration implications based on location events.",
            verbose=True
        )

    @task
    def working_location_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a Google Calendar working location event with the following structure:
            - result.id: Event ID
            - result.summary: Location description (e.g., "Casa" for home)
            - result.start.date: Start date (all-day event format)
            - result.end.date: End date (all-day event format)
            - result.eventType: "workingLocation"
            - result.workingLocationProperties: Object containing location details
              - result.workingLocationProperties.type: Location type (homeOffice, office, etc.)
            - result.transparency: Usually "transparent" for location events
            - result.recurringEventId: If part of a recurring pattern

            IMPORTANT: Extract the following information:

            1. Working Location Details:
               - Event ID and summary
               - Location type from workingLocationProperties.type
               - Date range (start.date to end.date)
               - Transparency setting

            2. Work Arrangement Analysis:
               - Type of working location (home office, office, custom)
               - Duration of the working arrangement
               - Recurring pattern if applicable
               - Work schedule implications

            3. Business Context:
               - Remote work pattern analysis
               - Team collaboration impact
               - Hybrid work schedule assessment
            """,
            expected_output="""
            A structured analysis containing:
            - Event Information:
              * Event ID: [Calendar event ID]
              * Summary: [Location description]
              * Event Type: [workingLocation]
              * Date Range: [start date to end date]
            - Working Location Details:
              * Location Type: [homeOffice, office, custom]
              * Location Properties: [detailed location info]
              * Transparency: [event transparency setting]
              * Recurring: [recurring pattern if applicable]
            - Work Arrangement Analysis:
              * Work Mode: [remote, hybrid, office]
              * Duration: [length of arrangement]
              * Schedule Impact: [team collaboration implications]
              * Pattern Analysis: [work-from-home frequency]
            """,
            agent=self.working_location_analyzer
        )

    @task
    def working_location_summarization_task(self) -> Task:
        return Task(
            description="""
            Create a comprehensive summary of the working location event that includes location type,
            dates, and insights into remote work patterns and team collaboration implications.
            """,
            expected_output="""
            A working location event summary in markdown format:
            - **Event ID**: Calendar event ID
            - **Location**: Location description and type
            - **Date Range**: Start and end dates
            - **Work Mode**: Remote/hybrid/office designation
            - **Location Type**: Specific location classification
            - **Duration**: Length of working arrangement
            - **Summary**: Overview of work location event
            - **Work Pattern**: Remote work pattern analysis
            - **Team Impact**: Collaboration and availability implications
            - **Schedule Notes**: Any recurring patterns or special considerations
            """,
            agent=self.working_location_summarizer,
            output_file='working_location_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GoogleCalendarWorkingLocationTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = GoogleCalendarWorkingLocationTrigger().crew()
    # Example payload from event-started.json
    crewai_trigger_payload = """{
        "result": {
            "created": "2025-03-24T13:52:31.000Z",
            "creator": {
                "email": "[REDACTED]",
                "self": true
            },
            "end": {
                "date": "2025-09-04"
            },
            "eventType": "workingLocation",
            "id": "[REDACTED]",
            "kind": "calendar#event",
            "start": {
                "date": "2025-09-03"
            },
            "status": "confirmed",
            "summary": "Casa",
            "transparency": "transparent",
            "workingLocationProperties": {
                "homeOffice": {},
                "type": "homeOffice"
            }
        }
    }"""
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
