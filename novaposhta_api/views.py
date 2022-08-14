from django.http import HttpResponse

from novaposhta_api.novaposhta import Novaposhta


def testview(request):
    np: Novaposhta = Novaposhta()
    np.update_data()
    return HttpResponse()
