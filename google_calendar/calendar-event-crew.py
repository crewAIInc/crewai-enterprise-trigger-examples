from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class GoogleCalendarEventTrigger:
    """GoogleCalendarEventTrigger crew"""

    @agent
    def calendar_event_analyzer(self) -> Agent:
        return Agent(
            role="Google Calendar Event Payload Parser and Analyzer",
            goal="Parse Google Calendar event payload data to extract event details (title, dates, attendees, location) and analyze event information for insights",
            backstory="You're an expert at parsing Google Calendar API payload structures and event data formats. You excel at navigating complex JSON structures to extract event information including summary, start/end times, attendees, location, description, and status. You understand different event types, recurrence patterns, and timezone handling in calendar events.",
            verbose=True
        )

    @agent
    def calendar_event_summarizer(self) -> Agent:
        return Agent(
            role="Calendar Event Summarization Specialist",
            goal="Create clear, concise summaries that prominently display event title, date/time, and attendees, then capture essential event details and context",
            backstory="You're a skilled communicator who specializes in distilling complex calendar event information into clear, actionable summaries. You excel at organizing information with event title and timing prominently displayed at the top, followed by comprehensive event analysis. You understand that event title, date/time, and attendees are the most critical pieces of information for quick event identification.",
            verbose=True
        )

    @task
    def calendar_event_analysis_task(self) -> Task:
        return Task(
            description="""
            The payload contains a Google Calendar event with the following structure:
            - result.id: Event ID
            - result.summary: Event title/name
            - result.start: Start date/time with timezone
            - result.end: End date/time with timezone
            - result.attendees[]: Array of attendee objects with email and response status
            - result.organizer: Event organizer information
            - result.location: Event location (if specified)
            - result.description: Event description/details
            - result.status: Event status (confirmed, tentative, cancelled)

            IMPORTANT: Extract the following information from the payload structure:

            1. Event Basic Information:
               - Event ID (result.id)
               - Event title (result.summary)
               - Event status (result.status)
               - Event type (result.eventType)

            2. Date and Time Information:
               - Start date/time (result.start.dateTime or result.start.date)
               - End date/time (result.end.dateTime or result.end.date)
               - Timezone information (result.start.timeZone, result.end.timeZone)
               - Duration calculation

            3. People and Organization:
               - Organizer information (result.organizer)
               - Attendees list (result.attendees) with response status
               - Creator information (result.creator)

            4. Event Details:
               - Location (result.location)
               - Description (result.description)
               - Visibility settings
               - Reminder settings (result.reminders)

            5. Analyze the event for:
               - Event purpose and type
               - Importance level based on attendees and content
               - Time conflicts or scheduling considerations
               - Action items or preparation needed
            """,
            expected_output="""
            A structured analysis containing:
            - Event Information:
              * Event ID: [Google Calendar event ID]
              * Title: [event summary/title]
              * Status: [event status]
              * Type: [event type]
            - Schedule Details:
              * Start: [start date/time with timezone]
              * End: [end date/time with timezone]
              * Duration: [calculated duration]
              * Timezone: [timezone information]
            - Participants:
              * Organizer: [organizer name and email]
              * Attendees: [list of attendees with response status]
              * Creator: [event creator information]
            - Event Details:
              * Location: [event location if specified]
              * Description: [event description/agenda]
              * Reminders: [reminder settings]
            - Analysis:
              * Event purpose and context
              * Importance assessment
              * Scheduling considerations
              * Preparation requirements
            """,
            agent=self.calendar_event_analyzer
        )

    @task
    def calendar_event_summarization_task(self) -> Task:
        return Task(
            description="""
            Based on the calendar event analysis from the parsed Google Calendar payload, create a comprehensive summary that includes:
            - The event title extracted from the "summary" field in the payload
            - The date/time information extracted from the "start" and "end" fields
            - The attendee and organizer information from the payload
            - Key event details and context from the analysis
            - Any important scheduling or preparation information
            - Assessment of event importance and type

            IMPORTANT: Ensure the event title (from "summary" field) and date/time (from "start"/"end" fields)
            are displayed prominently at the top of your summary. These are critical pieces of
            information that must be clearly visible for quick event identification.
            """,
            expected_output="""
            A well-structured calendar event summary in markdown format containing:
            - **Event ID**: Google Calendar event ID (from result.id in payload)
            - **Title**: Event title (extracted from "summary" field)
            - **Date & Time**: Start and end times with timezone (extracted from "start"/"end" fields)
            - **Status**: Event status (extracted from "status" field)
            - **Organizer**: Event organizer name and email
            - **Attendees**: List of attendees with response status
            - **Location**: Event location (if specified)
            - **Description**: Event description/agenda details
            - **Summary**: Concise overview of the event purpose
            - **Key Details**: Important information and context
            - **Preparation**: Any action items or preparation needed
            - **Priority**: Assessment of event importance

            Ensure the Title and Date & Time fields are prominently displayed at the top and
            formatted as clean markdown without code blocks.
            """,
            agent=self.calendar_event_summarizer,
            output_file='calendar_event_summary.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the GoogleCalendarEventTrigger crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )

if __name__ == "__main__":
    crew = GoogleCalendarEventTrigger().crew()
    crewai_trigger_payload = "PUT YOUR TRIGGER PAYLOAD HERE"
    crew.kickoff({'crewai_trigger_payload': crewai_trigger_payload})
