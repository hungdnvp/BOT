from datetime import datetime

def sample_response(input):
  user_mess = str(input).lower()

  if user_mess in ("hi", "hello", "ok"):
    return "Hi Bro :v"
  if user_mess in ("time", "time?"):
    now = "Hôm nay là: " + datetime.now().strftime("%d-%m-%y, %H:%M:%S")
    return str(now)
  ## Có thể thêm các câu hỏi mà người dùng nhập vào ở đây
  
  return "Hỏi gì đó khác đi bro? Hỏi khó như này thì chịu rồi :<"
