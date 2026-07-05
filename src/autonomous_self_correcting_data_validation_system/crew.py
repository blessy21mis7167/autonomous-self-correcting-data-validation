import os


from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	FileReadTool
)






@CrewBase
class AutonomousSelfCorrectingDataValidationSystemCrew:
    """AutonomousSelfCorrectingDataValidationSystem crew"""

    
    @agent
    def input_intake_preprocessing_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["input_intake_preprocessing_specialist"],
            
            
            tools=[				FileReadTool()],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def structured_field_extraction_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["structured_field_extraction_specialist"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def business_rules_schema_rag_retrieval_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["business_rules_schema_rag_retrieval_specialist"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def data_integrity_validation_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["data_integrity_validation_specialist"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def validation_error_classification_risk_assessment_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["validation_error_classification_risk_assessment_specialist"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def deterministic_data_auto_correction_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["deterministic_data_auto_correction_specialist"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def data_quality_confidence_scoring_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["data_quality_confidence_scoring_specialist"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def human_in_the_loop_verification_escalation_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["human_in_the_loop_verification_escalation_specialist"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def final_quality_assurance_schema_compliance_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["final_quality_assurance_schema_compliance_specialist"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    
    @agent
    def compliance_audit_trail_validation_report_specialist(self) -> Agent:
        
        
        return Agent(
            config=self.agents_config["compliance_audit_trail_validation_report_specialist"],
            
            
            tools=[],
            
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            
            
            max_execution_time=None,
            llm=LLM(
                model="openai/gpt-4o-mini",
                
                
            ),
            
        )
        
    

    
    @task
    def intake_and_normalize_raw_input(self) -> Task:
        return Task(
            config=self.tasks_config["intake_and_normalize_raw_input"],
            markdown=False,
            
            
        )
    
    @task
    def extract_and_type_structured_fields(self) -> Task:
        return Task(
            config=self.tasks_config["extract_and_type_structured_fields"],
            markdown=False,
            
            
        )
    
    @task
    def retrieve_validation_rules_from_knowledge_base(self) -> Task:
        return Task(
            config=self.tasks_config["retrieve_validation_rules_from_knowledge_base"],
            markdown=False,
            
            
        )
    
    @task
    def validate_all_extracted_fields(self) -> Task:
        return Task(
            config=self.tasks_config["validate_all_extracted_fields"],
            markdown=False,
            
            
        )
    
    @task
    def classify_validation_errors_by_correction_tier(self) -> Task:
        return Task(
            config=self.tasks_config["classify_validation_errors_by_correction_tier"],
            markdown=False,
            
            
        )
    
    @task
    def apply_auto_corrections_and_build_correction_log(self) -> Task:
        return Task(
            config=self.tasks_config["apply_auto_corrections_and_build_correction_log"],
            markdown=False,
            
            
        )
    
    @task
    def compute_field_and_record_confidence_scores(self) -> Task:
        return Task(
            config=self.tasks_config["compute_field_and_record_confidence_scores"],
            markdown=False,
            
            
        )
    
    @task
    def request_human_verification_for_blocked_fields(self) -> Task:
        return Task(
            config=self.tasks_config["request_human_verification_for_blocked_fields"],
            markdown=False,
            
            
        )
    
    @task
    def final_quality_assurance_and_schema_compliance_check(self) -> Task:
        return Task(
            config=self.tasks_config["final_quality_assurance_and_schema_compliance_check"],
            markdown=False,
            
            
        )
    
    @task
    def generate_audit_log_and_validation_report(self) -> Task:
        return Task(
            config=self.tasks_config["generate_audit_log_and_validation_report"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the AutonomousSelfCorrectingDataValidationSystem crew"""

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,

            chat_llm=LLM(model="openai/gpt-4o-mini"),
        )


