from django.shortcuts import get_object_or_404
from ninja import Router
from apps.main.models import FAQ
from apps.blog_api.schemas.faq import FAQSchema, FAQCreateSchema

faqs_router = Router(tags=['Faqs'])


@faqs_router.get('/api/faqs/', response=list[FAQSchema])
def get_faqs(request):
    faqs = FAQ.objects.all()
    return faqs


@faqs_router.post('/api/faqs/', response=FAQSchema)
def create_faq(request, data: FAQCreateSchema):
    is_question_exists = FAQ.objects.filter(question=data.question)
    if is_question_exists.exists():
        obj = is_question_exists.first()
        obj.answer = data.answer
        obj.save()
        return obj

    new_faq = FAQ.objects.create(**data.model_dump())
    return new_faq


@faqs_router.delete('/api/faqs/{faq_id}/')
def delete_faq(request, faq_id: int):
    faq = get_object_or_404(FAQ, pk=faq_id)
    faq.delete()
    return {'success': True}
