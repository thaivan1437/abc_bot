#!/usr/bin/env python3
import base64
import json

def decode_and_save():
    """Decode và lưu kết quả vào file"""
    
    # Đoạn mã gốc
    encoded_data = "VUxQS1oJKBdGXRYCCRZNWwJdVgFRRwEBVgwBGRZeVQ5TBlhRSEVZVUNNRjpPSVBGW0ZIRUBbfUFNTAxiBFNNQlReARgAHB1WaxUXCQABBw9gRl5BXh0UA24fQxALA1EWCxseXwYJBlRUX0YLUUJUQgxUBhUXFwQfAQRAFgseAkxXVFoRDwdGXQUEAR4eQhRdUAUFUV5XGBZGQVsAUlxRRltDSEVcRBMUHkIUWEEQABAPRQ4EHQxKC1BcWxcEUV5XGBZCS19MDAlISBpRBwhQURMUG14HCQVVUUdIRVhRR0tCTAwJGUYSFggCV0ATFB5CFFhYCxQdEEUOBB0MSgtXXRdeUV9GEFtBX0pLChQDBUhDGxRFDgQdDE8aQlhWD0NJVEsWUFRISwBFXBdeUV9GFFFFExQeExpCFwcOFwFFDgEBHx5eBAkBSEMfARFRWBMUHkIUSlAIBBAQRQ4EHQxPA1lMWxBDSVRLFlBUT0pMDAkZRhYcEQlQUVUMFF4aG10UQ0lUSxZVRVpPDV0bD1RNUQACUlFfXUtMDAkZRhIWFUUOBEwCVUxVVlEBQ0lRVwUEAR0eWhobWQEXFghFDgQdDF0LWlxWEENJVEsWVVxBWwBCGw9UTVEAAlVQExQeQhROWhEPFwEDFg4BAgwGRhsPVE1RBRNAVVJFDFQGFRcABBUBCUdRExQeQhRKUBVDSVQaGE8TTUEKUxsPUVFCVFcFBAICDAJTT1AIQ0lUSxZHVEJLDUIbD1RNUQUKW0FfWgxUBhUXAAQSAEUOBB0MWQFDV1EBBVFeVxgWWV4MVAYVFwUVBwUEXxYLHgJMUlxTAQ8AAUUOBB0MXQtHGw9UHF8fRVdbVUsMVAMJBFRRQVRUGBZdS1gLWhsPVE1RFwJYUVJaDFQGFRcFDBwRCUAWCx4CTFJcVABDSVRLFkNeW0AKU10XXlFfRg9EFgseAkxXTUEFAhhGXQQYE0pLCFNXRgFDSVRLFkdUXwxUBkQZH0MQCwNRFgsbHl8GCQZUUl9GC1FCVEIMVAYVFxcEHwEEQBYLHgJMV1RaEQ8HRl0EGBNKSw9SGw9UTVETCEFaVUtKTAwJGUYJA0ZdBBgTT1oaV1peRltDSEVQUVdLQB1TGw9UTVEXAkUWCx5TQk0bVgsFFkZdAQQAHh5fBgsZRg0WEgJYFgseAkxFXFkBAgdGXQQYE09DAUNXQUZbQ0hFUFFQSgxUBhUXEw4GCgNRUBMUHkIUUUVGW0NIRVVARU9NBRQDBUhDFwEBUVpCSwxUBhUXFwQCRl0ESR1VDA1ZXVBGW0ZUVgQEAx4cQhRVUBIEH0ZdBBgTXUsCU1pBRltDSEVVWV5bQBoUAwVIQxcBBlAWCx4CTEFWQAoFFgBFDgQdDEYeFAMFSEMSEBNVV1oMFF4aG1EBBxYKFFEWCx4CTEVcREZbQxlLTxZSQUoLFAMAVFBDVFQEBh0MQgtAXFlGW0NIRUdRXUtNGhQDBUhDEgkIQVpFDBReGhtRAQAXRl0EGBNZQRtYXVAAQ0lUSxZcQQwUXhobVBAVEgcMFg4BAgwKU19QChIWRl0EGBNdSx8UAwUZPA4="
    
    # Password XOR
    xor_password = ".n695dasdg441."
    
    print("🔓 Đang decode...")
    
    # Decode
    b64_decoded = base64.b64decode(encoded_data)
    xor_decoded = bytearray([
        each_byte ^ ord(xor_password[index % len(xor_password)])
        for index, each_byte in enumerate(b64_decoded)
    ])
    decoded_str = xor_decoded.decode('utf-8')
    result = json.loads(decoded_str)
    
    print("✅ Decode thành công!")
    
    # Lưu vào file JSON
    with open('decoded_result.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    # Lưu vào file text với format đẹp
    with open('decoded_result.txt', 'w', encoding='utf-8') as f:
        f.write("=== KẾT QUẢ DECODE ĐOẠN MÃ LOK BOT ===\n\n")
        f.write(f"Password XOR: {xor_password}\n")
        f.write(f"Độ dài dữ liệu: {len(b64_decoded)} bytes\n\n")
        
        f.write("=== THÔNG TIN CHÍNH ===\n")
        f.write(f"From ID: {result['fromId']}\n")
        f.write(f"March Type: {result['marchType']}\n")
        f.write(f"To Location: {result['toLoc']} (X={result['toLoc'][0]}, Y={result['toLoc'][1]}, Z={result['toLoc'][2]})\n\n")
        
        f.write("=== THÔNG TIN QUÂN ĐỘI ===\n")
        for i, troop in enumerate(result['marchTroops']):
            if troop['amount'] > 0:
                f.write(f"Troop {i+1}:\n")
                f.write(f"  - Code: {troop['code']}\n")
                f.write(f"  - Level: {troop['level']}\n")
                f.write(f"  - Amount: {troop['amount']:,}\n")
                f.write(f"  - HP: {troop['hp']}\n")
                f.write(f"  - Attack: {troop['attack']}\n")
                f.write(f"  - Defense: {troop['defense']}\n\n")
        
        f.write("=== DỮ LIỆU JSON ĐẦY ĐỦ ===\n")
        f.write(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("📁 Đã lưu kết quả vào:")
    print("   - decoded_result.json (format JSON)")
    print("   - decoded_result.txt (format text đẹp)")
    
    return result

if __name__ == "__main__":
    decode_and_save()