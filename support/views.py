from django.shortcuts import render
from .forms import ChatForm
from .models import Chat

def chatbot(request):
    form = ChatForm()

    if request.method == "POST":
        form = ChatForm(request.POST)

        if form.is_valid():
            text = form.cleaned_data["message"]

            Chat.objects.create(
                user=request.user if request.user.is_authenticated else None,
                question=text
            )

            return render(
                request,
                "support/chat.html",
                {
                    "form": ChatForm(),
                    "reply": "پیام شما ثبت شد. به زودی پاسخ می‌دهیم."
                }
            )

    return render(
        request,
        "support/chat.html",
        {
            "form": form
        }
    )