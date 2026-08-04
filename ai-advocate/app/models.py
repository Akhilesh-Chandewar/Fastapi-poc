from pydantic import BaseModel, Field
from datetime import datetime

class Contract(BaseModel):
    contract_id: str = ""
    file_name: str
    original_file_name: str
    uploaded_date: str = ""
    text_content: str = ""
    page_count: int = 0
    word_count: int = 0
    status: str = "uploaded"  # Possible values: uploaded, processed, error

    def model_post_init(self, _context):
        if not self.uploaded_date:
            self.uploaded_date = datetime.now().isoformat()


class ContractUploadResponse(BaseModel):
    message: str
    contract: Contract
    id: str
