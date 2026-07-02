#day 16


from agents.extraction_agent import ExtractionAgent
from agents.analysis_agent import AnalysisAgent
from agents.verification_agent import VerificationAgent
import time

class Coordinator:

    def __init__(self):
        #creating 3 objects
        self.extraction = ExtractionAgent()
        self.analysis = AnalysisAgent()
        self.verification = VerificationAgent()

        
    def handle_request(self, request):
        request = request.lower()
        
        #routing

                # Extraction Agent
        if "email" in request:
            print("➡ Calling: ExtractionAgent.extract_emails()")
            return self.extraction.extract_emails(request)

        elif "phone" in request:
            print("➡ Calling: ExtractionAgent.extract_phone_numbers()")
            return self.extraction.extract_phone_numbers(request)

        elif "name" in request:
            print("➡ Calling: ExtractionAgent.extract_names()")
            return self.extraction.extract_names(request)

        elif "extract" in request:
            print("➡ Calling: ExtractionAgent.extract_data()")
            return self.extraction.extract_data(request)

        # Analysis Agent
        elif "summary" in request or "summarize" in request:
            print("➡ Calling: AnalysisAgent.summarize()")
            return self.analysis.summarize(request)

        elif "analyze" in request:
            print("➡ Calling: AnalysisAgent.analyze_document()")
            return self.analysis.analyze_document(request)

        elif "classify" in request:
            print("➡ Calling: AnalysisAgent.classify_document()")
            return self.analysis.classify_document(request)

        # Verification Agent
        elif "verify" in request:
            print("➡ Calling: VerificationAgent.verify()")
            return self.verification.verify(request)

        elif "fact" in request:
            print("➡ Calling: VerificationAgent.fact_check()")
            return self.verification.fact_check(request)

        elif "validate" in request:
            print("➡ Calling: VerificationAgent.validate_document()")
            return self.verification.validate_document(request)

        elif "quality" in request:
            print("➡ Calling: VerificationAgent.quality_check()")
            return self.verification.quality_check(request)

        else:
            print("➡ No matching tool found")
            return "Unknown request"


if __name__ == "__main__":

    coordinator = Coordinator()

    start = time.perf_counter()

    print(coordinator.handle_request(
    "Extract names from this resume"
    ))
    
    # print(coordinator.handle_request(
    #     "Extract email from this resume"
    # ))
    
    # print(coordinator.handle_request(
    #     "Summarize this report"
    # ))
    
    # print(coordinator.handle_request(
    #     "Analyze this document"
    # ))
    
    # print(coordinator.handle_request(
    #     "Verify this statement"
    # ))

    end = time.perf_counter()

    
    print(f"Latency: {end-start:.6f} seconds")


    
