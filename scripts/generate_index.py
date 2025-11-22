import os
import json
from datetime import datetime

# Cấu hình đường dẫn
PAGES_DIR = 'pages'
INDEX_FILE = 'index.json'

def generate_sitemap():
    library = {
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_pages": 0,
        "pages": []
    }

    # Kiểm tra nếu thư mục pages tồn tại
    if not os.path.exists(PAGES_DIR):
        print(f"Directory {PAGES_DIR} not found.")
        return

    # Quét từng thư mục con trong /pages/
    # sorted() giúp danh sách ổn định, không bị nhảy thứ tự mỗi lần chạy
    for book_folder in sorted(os.listdir(PAGES_DIR)):
        book_path = os.path.join(PAGES_DIR, book_folder)
        
        # Chỉ xử lý nếu là thư mục
        if os.path.isdir(book_path):
            book_data = {
                "id": book_folder,
                "info": {},
                "chapters": []
            }

            # 1. Đọc file metadata.json nếu có
            meta_path = os.path.join(book_path, 'metadata.json')
            if os.path.exists(meta_path):
                try:
                    with open(meta_path, 'r', encoding='utf-8') as f:
                        book_data["info"] = json.load(f)
                except Exception as e:
                    print(f"Error reading metadata for {book_folder}: {e}")
            else:
                # Nếu không có metadata, tạo info mặc định từ tên thư mục
                book_data["info"] = {
                    "title": book_folder.replace('_', ' ').title(),
                    "id": book_folder
                }
            
            # 2. Quét các file nội dung (.txt hoặc .md)
            # Loại bỏ metadata.json và các file ẩn
            valid_extensions = ('.txt', '.md')
            
            for file in sorted(os.listdir(book_path)):
                if file.endswith(valid_extensions) and file != 'metadata.json':
                    book_data["chapters"].append({
                        "filename": file,
                        "path": f"{PAGES_DIR}/{book_folder}/{file}"
                    })
            
            # Chỉ thêm vào danh sách nếu thư mục có chứa chương hoặc metadata
            if book_data["chapters"] or book_data["info"]:
                library["pages"].append(book_data)

    library["total_pages"] = len(library["pages"])

    # Ghi ra file index.json
    try:
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            json.dump(library, f, indent=2, ensure_ascii=False)
        print(f"Sitemap ({INDEX_FILE}) updated successfully with {library['total_pages']} items.")
    except Exception as e:
        print(f"Error writing index file: {e}")

if __name__ == "__main__":
    generate_sitemap()
