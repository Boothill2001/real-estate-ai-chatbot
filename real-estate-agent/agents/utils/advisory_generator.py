# === agents/utils/advisory_generator.py ===
def generate_advisory(listings):
    if not listings:
        return "Hiện tại mình chưa tìm được căn phù hợp. Bạn có muốn mình tìm thêm không? 😊"
    
    advisory_text = "🏡 Dựa trên yêu cầu của bạn, mình gợi ý căn sau:\n\n"

    for idx, listing in enumerate(listings, 1):
        advisory_text += f"⭐ Lựa chọn {idx}:\n{listing}\n\n"

    advisory_text += "✨ Đây là những căn có giá hợp lý, diện tích ổn, và lease start tốt.\nNếu cần mình hỗ trợ thêm, cứ hỏi nhé! 👌"
    return advisory_text