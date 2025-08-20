# CrewAI Enterprise Trigger Payload Samples

This repository contains examples of Trigger payloads to help you develop Automation Triggers check it out [here](https://docs.crewai.com/en/enterprise/guides/automation-triggers). All data has been sanitized and replaced with safe, non-sensitive sample values for development and testing.

## 📁 Repository Structure

```
gmail/
├── new-email-payload-1.json      # Database connection error alert
├── new-email-payload-2.json      # Performance warning alert
└── thread-updated-sample-1.json  # Deployment failure alert
```

## 📧 Sample Scenarios

### New Email Payloads

#### `new-email-payload-1.json` - Database Connection Error
- **Scenario**: Critical database connection pool exhaustion
- **Service**: AlertService from payment gateway
- **Alert Level**: Critical
- **Environment**: Production
- **Key Features**: Complete SMTP headers, authentication results, alert details

#### `new-email-payload-2.json` - Performance Warning
- **Scenario**: High response times in user authentication endpoint
- **Service**: MonitoringService from user API
- **Alert Level**: Warning
- **Environment**: Production
- **Key Features**: Performance metrics, recommendations, SLA breach details

### Thread Updated Payloads

#### `thread-updated-sample-1.json` - Deployment Failure
- **Scenario**: Kubernetes pod startup failure during rolling update
- **Service**: AlertService from API gateway
- **Alert Level**: Critical
- **Environment**: Production
- **Key Features**: Deployment logs, rollback information, Kubernetes events
