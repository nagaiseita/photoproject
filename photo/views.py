from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView,DetailView, DeleteView
from django.urls import reverse_lazy
from .forms import PhotoPostForm
from .models import PhotoPost
#以下2つはログイン状態でviewを呼び出すためのもの
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class IndexView(ListView):
    #index.htmlを指定する
    template_name = 'index.html'
    
    #モデルの指定
    #投稿日順(posted_at)に並べ替える(新しい順;降順)
    queryset = PhotoPost.objects.order_by('-posted_at')

    #1ページに表示するデータの数
    paginate_by = 9    

#ログイン状態の時のみ以下のviewを使えるようにする
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    #フォーム（入力項目）の設定
    form_class = PhotoPostForm
    #描画するHTMLファイル
    template_name = 'post_photo.html'
    #データ登録後に移る（リダイレクトされる）ページ
    success_url = reverse_lazy('photo:post_done')
    
    #入力されたデータ（画像含む）をモデルに保存
    def form_valid(self, form):
        #送信されてきた(POSTされた)データを取得
        postdata = form.save(commit=False)
        #投稿(ログインしている)ユーザをpostdataのユーザに代入
        postdata.user = self.request.user
        #データベースに保存
        postdata.save()
        
        return super().form_valid(form)

class PostSuccessView(TemplateView):
    #描画するHTMLファイル
    template_name = 'post_success.html'

class CategoryView(ListView):
    #描画するHTML
    template_name = 'index.html'
    #1ページに表示するレコードの件数
    paginate_by = 6
    #クリックされたカテゴリの一覧を返す関数
    def get_queryset(self):
        #クリックされたカテゴリのidを取得
        category_id = self.kwargs['category']
        #上記で取得したidのデータのみ抽出
        records = PhotoPost.objects.filter(
            category=category_id).order_by('-posted_at')
        #取得したレコードを返す
        return records

class UserView(ListView):
    #描画するHTML
    template_name = 'index.html'
    #1ページに表示するレコードの件数
    paginate_by = 6
    #クリックされたカテゴリの一覧を返す関数
    def get_queryset(self):
        #クリックされたカテゴリのidを取得
        user_id = self.kwargs['user']
        #上記で取得したidのデータのみ抽出
        records = PhotoPost.objects.filter(
            user=user_id).order_by('-posted_at')
        #取得したレコードを返す
        return records

class PhotoDetailView(DetailView):
    #描画するHTML
    template_name = 'detail.html'
    #使用するデータベース(モデル)の指定
    model = PhotoPost

class MypageView(ListView):
    #描画するHTML
    template_name = 'mypage.html'
    #1ページに表示するレコードの件数
    #paginate_by = 6
    #ログインしているユーザの投稿写真一覧を返す関数
    def get_queryset(self):
        records = PhotoPost.objects.filter(
            user=self.request.user).order_by('-posted_at')
        #取得したレコードを返す
        return records

class PhotoDeleteView(DeleteView):
    #描画するHTMLファイル
    template_name = 'photo_delete.html'
    #参照するデータベース(モデル)
    model = PhotoPost
    #削除完了後に移る(リダイレクトする)ページ
    success_url = reverse_lazy('photo:mypage')