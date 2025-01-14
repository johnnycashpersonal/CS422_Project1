# Initial Project Plan & SDS
# Project Plan

A management plan. How is your team organized? How is the work divided among team members? How does your team make decisions? How will your team meet and how will it communicate.
- Tasks are divided based on expertise and interest to maximize efficiency:

**Team Organization:**
*John*: Backend Developer
- Manages data processing and sets up the database architecture.
Develops and optimizes queries to efficiently gather and process data from the database.

*Manu*: Frontend Developer
- Designs and implements the user interface using Tkinter to ensure usability and an optimized user experience.
- Integrates data visualizations and filtering options into the frontend.

*Tim*: Admin Instructions
- Develops backend controls and tools for system administrators, including database integration and advanced processing features.
- Ensures admin utilities are intuitive and provide seamless data management.

*Myles*: Faculty Features and Advanced Data Views
- Implements faculty-related features, such as filtering by department, course level, and faculty type.
- Designs and builds side-by-side comparison visualizations for faculty grading distributions.
- Creates advanced data views, ensuring they are clear, comprehensive, and user-friendly.



**Decision-Making:**
Decisions are made collaboratively during weekly meetings. If a question needs to be answered more quikly they can be donw so through the shared groupchat.

Communication:
- Weekly meetings will be conducted at a time fit for everyone (virtual/in-person) to discuss progress and next steps.
- Day-to-day communication will take place over text groupchat, and emails used for sharing documents.
- GitHub will be used for version control, task tracking, and code reviews.


**Work breakdown schedule**

**Phase 1: Project Planning and Design (Jan 13–17):**
- Finalize system architecture and database schema.(JOHN)
- Create initial UI wireframes.(MANU)

Prepare and submit project documentation. (TEAM)

**Phase 2: Foundation Development (Jan 18–22):**
- Set up the MongoDB environment. (JOHN/MANU)
- Implement database connection utilities (JOHN/MANU)
- Create and validate the initial database schema (JOHN/MANU)

**Phase 3: Core Features Development (Jan 23–27):**
- Develop the Tkinter GUI framework (MANU)
- Implement basic data querying capabilities
- Integrate data visualization (MYLES)

**Phase 4: Advanced Features (Jan 28–31):**
- Add advanced filtering and comparison tools (MYLES)
- Implement side-by-side visualizations (MYLES)
- Develop admin tools for data management (TIM)

**Phase 5: Testing and Refinement (Feb 1–4):**
- Conduct unit and integration tests (TEAM)
- Optimize performance and debug (TEAM)
- Finalize user and admin documentation (TIM) 




**Tracking Individual and Project Progress:**

GitHub will be used to track contributions via commits, pull requests, and task assignments.
Github Projects will be used for task management and milestone tracking.

Reporting Progress:
Weekly progress scrums will be prepared by each team member summarizing completed tasks, ongoing work, and blockers.

Documentation:
Each team member is responsible for documenting their contributions, including code comments, test results, and decision logs.




## EasyA Project Build Plan

The Project will be executed in five main phases from January 13th to February 5th, 2024.

**Phase 1: Project Planning and Design (Jan 13-17)**

- First we will establish the system architecture, database schema, and user interface design. 
- This phase concludes with the January 17th documentation deadline for Project Plan and SDS Submission.

**Phase 2: Foundation Development (Jan 18-22)**

- Includes setting up the local MongoDB environment, creating the database management system, and building data processing utilities. 
- Focus will be on establishing robust data handling capabilities and implementing the basic data models that will support all future development.

**Phase 3: Core Features Development (Jan 23-27)**

- includes implementing the Tkinter GUI framework, creating basic matplotlib visualizations, and establishing core data querying capabilities. 
- users will be able to view basic grade distributions and perform fundamental data filtering.

**Phase 4: Advanced Features (Jan 28-31)**

- Includes side-by-side comparison view, detailed filtering options, and administrator tools. 
- This phase will also see the implementation of comprehensive error handling and data management features for system administrators.

**Phase 5: Testing and Refinement (Feb 1-4)**

- includes comprehensive unit and integration testing, performance optimization, and documentation completion. 
- concludes with the preparation of the final submission package and presentation materials.

**Timeline and Deliverables**

- Build 0.1 (Jan 13-17): Project planning and documentation
- Build 1.0-1.1 (Jan 18-22): Data infrastructure and processing
- Build 2.0-2.1 (Jan 23-27): Core visualization and interface features
- Build 3.0-3.1 (Jan 28-31): Advanced features and admin tools
- Build 4.0-4.1 (Feb 1-4): Testing, refinement, and final preparation

**Quality Assurance**

- Continuous testing and validation. Each build must pass functional testing, maintain data integrity, and meet performance requirements before proceeding to next goal.
- Regular code reviews and documentation updates will ensure maintainability and clarity throughout development.

**Dependencies**

- Python 3.x
- MongoDB
- Tkinter
- Matplotlib
- PyMongo

## Build Plan Rationale

**Development Approach**

- All visualization and analysis features depend on reliable data processing and storage. By establishing a solid data foundation early, we reduce the risk of major architectural changes later in development.

- Starting with core features before advancing to complex visualizations allows for early testing and validation of fundamental components. This approach ensures that basic functionality is robust before adding more sophisticated features, reducing the likelihood of systemic issues in the final product.

**Risk Analysis and Mitigation**

- Primary risks in this project center around data processing, technical integration, and feature completion. Data processing risks include potential inconsistencies in the grade data format and challenges in faculty name matching. 
- These risks are mitigated through early implementation of data validation and cleaning utilities in Phase 2.
- Technical risks primarily involve the integration of MongoDB with our visualization components and potential performance issues with large datasets. We address these through early performance testing and a modular development approach that allows for component isolation and targeted optimization.
- The tight timeline presents a feature completion risk, particularly for advanced visualization features. This is mitigated through clear feature prioritization and the inclusion of buffer time in the final phase for unexpected challenges.

**Build Sequence Justification** 

- Phase 1's focus on planning ensures that key architectural decisions are made before coding begins.
- Phase 2's emphasis on data infrastructure provides the foundation for all subsequent development.
- Phases 3 and 4 build progressively more complex features on this foundation, while Phase 5 ensures thorough testing and refinement.
- This sequential approach reduces integration complexity and minimizes the risk of major refactoring. The dedicated testing phase ensures a polished final product.

**Success Criteria**

 - The planning phase must produce comprehensive documentation and clear requirements. 
 - The foundation phase requires validated data processing and storage capabilities. 
 - Core and advanced feature phases must deliver working visualizations and user interface components. The final phase ensures all functionality meets performance requirements and is thoroughly tested.

## SDS
*Myles*
- A description of the product you intend to build. This should describe the externally visible behavior of your product as precisely as possible, but it should be concise and clear.
- An overall design description. What are the major parts of your system, and how do they fit together?
- System structure is clear.

*Tim*
- Each major subsystem should be explained using a separate static model and dynamic model. All diagrams must be clear and understandable.
- Design Rationale. Why did you chose this particular design? What are the main organizing principles that you used to break your system into parts?
