#!/usr/bin/env python
# coding: utf-8

# In[11]:


from flask import Flask, request, render_template
import pickle


# In[12]:


app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))
Cv = pickle.load(open('Cv.pkl', 'rb'))


# In[13]:


@app.route('/')
def home():
    return render_template('index.html')


# In[14]:


@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        text = request.form['Review']
        data = [text]
        vectorizer = Cv.transform(data).toarray()
        prediction = model.predict(vectorizer)
    if prediction:
        return render_template('index.html', prediction_text='The review is Postive')
    else:
        return render_template('index.html', prediction_text='The review is Negative.')


# In[15]:


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)


# In[ ]:




