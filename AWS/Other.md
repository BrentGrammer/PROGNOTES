# XRay
- Solves difficulty of seeing logs for debugging and testing/analyzing production and across multiple distributed services
- Get a visual analysis of your applications
  - **Distributed Tracing**
  - **Have and see a Service Graph of traces**
  - **Toubleshooting**
- Have to enable it on your services
- Use cases examples:
  - Toubleshoot performance (bottlenecks)
  - understand dependencies of a microservice architecture
  - pinpoint service issues
  - Review request behavior
  - Where is throttling happening?

# Amazon CodeGuru
- Machine Learning powered automated code reviews and application performance recommendations
- 2 functionalites:
  - CodeGuru Reviewer: automated code reviews for static code analysis
    - finds resource links, security holes, best practices violations and input validation problems
    - supports Java and Python, integrates with other source control platforms
  - CodeGuru Profiler: visibility and recommendations about application performance during **production runtime**. Identifies cost improvements etc.
    -  removes code ineffeciencies, reduces cpu utilization to save costs, anomaly detection

# AWS Status - Service Health Dashboard 
- Shows all regions and all services health - general services, not personalized
- Historical info for each day
- Option to subscrie to RSS feed
- status.aws.amazon.com
- **AWS Personal Health Dashboard**
  - provides alerts and remediation guidance when AWS expereinces events that may directly affect you and your deployment.
  - Personalized to show you how the events affect the AWS services related to your uses
  - has proactive notification to help you plan for scheduled activities
  - phd.aws.amazon.com