import base64
import time
from datetime import datetime

import pandas as pd
import pytz
import requests
import streamlit as st

SITE_LIST = ['hosted-sites.army.gr', 'armyold.army.gr', 'bebeosis.army.gr', 'mail.army.gr', 'forensics.army.gr',
             'spb.army.gr', '492gsn.army.gr', 'www.anfm.army.gr', 'nspa.army.gr', 'poseidon.army.gr',
             'alumnissas.army.gr', 'geetha.army.gr', 'emathisi.army.gr', '2fssas.army.gr', 'elearning-sey.army.gr',
             '20-www.army.gr.army.gr', 'army.gr', 'elearning-syp.army.gr', 'laed.army.gr', '424gsne.army.gr',
             'ethnofilaki.army.gr', 'elearning-diged.army.gr', '424gsn.army.gr', 'alumnisdiep.army.gr',
             'elearning-sem.army.gr', 'sypo.army.gr', 'prodiagrafes.army.gr', 'efedros.army.gr', '250-mailer.army.gr',
             'ova2020.army.gr', 'elearning.army.gr', '411gsn.army.gr', 'psmtests.army.gr', 'elearning-spb.army.gr',
             'caxmg.army.gr', 'anfm.army.gr', 'kex.army.gr', 'elearning-sth.army.gr', 'sas.army.gr', 'smy.army.gr',
             'eadispo.army.gr', 'adispo.army.gr', 'frourarxeioathinon.army.gr', 'saep.army.gr', 'spsx.army.gr',
             'alumnisse.army.gr', 'bbbsdiep.army.gr', 'sthad.army.gr', 'bebeosis-api.army.gr', 'efeth.army.gr',
             'bbb.army.gr', '2faooa.army.gr', '412gsn.army.gr', 'www.army.gr', '212kixne.army.gr',
             'ekath-hosted.army.gr', 'sse.army.gr', '20-www.army.gr', '414snen.army.gr', 'alumnisas.army.gr',
             'devpsmtests.army.gr', 'spz.army.gr', 'alumnisetha.army.gr', 'asye.army.gr', 'steatx.army.gr',
             'ekems.army.gr', 'elearning-sxo.army.gr', '414snenn.army.gr', '216kixne.army.gr', 'accounts.army.gr',
             'auctions.army.gr', 'crisis.army.gr', '219kixne.army.gr', 'elearning-des.army.gr', 'nna.army.gr',
             'steamx.army.gr', 'hagschat.army.gr', 'mailer.army.gr', 'katataxi.army.gr', 'nrdc.army.gr',
             '251gna.army.gr', 'dis.army.gr', 'espsx.army.gr', 'aooa.army.gr', 'dev.army.gr', 'esdiep.army.gr',
             '406gsn.army.gr', 'sse190.army.gr', '404gsn.army.gr', '496gsn.army.gr', 'army.gr.army.gr',
             'elearning-spz.army.gr', 'seap.army.gr', '417nimts.army.gr', 'esetha.army.gr', 'portal.army.gr',
             'setha.army.gr', '401gsn.army.gr', 'fww.army.gr', 'ekath.army.gr', 'alumnisan.army.gr', 'sxo.army.gr',
             'elearning-smy.army.gr', 'sphy.army.gr', 'sath.army.gr', 'sdb.army.gr', 'alumnismy.army.gr',
             'elearning-sas.army.gr', 'spider.army.gr', '2b-www.army.gr.army.gr', 'mpsotc.army.gr',
             'www.apografi.army.gr', '401.army.gr', 'alumniadispo.army.gr', 'sey.army.gr', 'medusa.army.gr',
             'mts.army.gr', 'ytes.army.gr', 'elearning-sdb.army.gr', 'asdys.army.gr', 'mytest.army.gr', 'dfp.army.gr',
             '2f401.army.gr', 'devbebeosis.army.gr', 'devbebeosis-api.army.gr', 'ssas.army.gr', 'apografi.army.gr',
             'smx.army.gr', 'disarxeio.army.gr', 'elearning-smx.army.gr', '3awww.army.gr', 'alumnispsx.army.gr',
             'san.army.gr', 'elearning-tx.army.gr', 'nnk.army.gr', 'parousiasi.army.gr', 'mip.army.gr',
             'webconf.army.gr', 'sdiep.army.gr', 'staging.army.gr', '401gsna.army.gr', 'gramasye.army.gr',
             'nns.army.gr', 'wargames.army.gr']

duration_ = []
results = []

data = pd.DataFrame()


def download_link(df_, download_filename, download_link_text):
    """
    Generates a link to download the given object_to_download.

    object_to_download (str, pd.DataFrame):  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
    download_link_text (str): Text to display for download link.

    Examples:
    download_link(YOUR_DF, 'YOUR_DF.csv', 'Click here to download data!')
    download_link(YOUR_STRING, 'YOUR_STRING.txt', 'Click here to download your text!')
    """

    if isinstance(df_, pd.DataFrame):
        file_to_download = df_.to_csv(index=False)
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(file_to_download.encode()).decode()
        return f'<a class="streamlit-button small-button primary-button" ' \
               f'style="text-decoration: none; color: #262730;" href="data:file/txt;base64,{b64}"' \
               f' download="{download_filename}">{download_link_text}</a>'


def get_status(site_):
    try:
        response = requests.head(site_, timeout=10)
        status_code = response.status_code
        reason = response.reason
    except requests.exceptions.ReadTimeout:
        status_code = '-'
        reason = 'Read timed out'
    except requests.exceptions.ConnectionError:
        status_code = '000'
        reason = 'ConnectionError'
    return site_, status_code, reason


st.title('Έλεγχος σελίδων στο domain army.gr')

urls = st.multiselect(
    'Παρακαλώ επιλέξτε τα urls που επιθυμείτε να γίνει έλεγχος:', SITE_LIST, SITE_LIST)

if st.button('Check sites'):
    if st.button('Stop checking'):
        st.stop()
    # Add a placeholder
    latest_iteration = st.empty()
    bar = st.progress(0)

    for url in urls:
        start = time.time()
        site = 'http://{}'.format(url)
        if get_status(site)[1] in [301, 302, 303]:
            site = 'https://{}'.format(url)
        latest_iteration.text(f'Checking site {site}')
        bar.progress((urls.index(url) + 1) / len(urls))
        stop = time.time()
        duration = stop - start
        duration_.append(duration)
        results.append(get_status(site))

    st.header('Εμφάνιση αποτελεσμάτων')

    df = pd.DataFrame(data=results, columns=[
        'site', 'status_code', 'reason'], index=None)
    data = df.copy()

    if len(df[df.status_code == '000']) > 0:
        st.header('Εμφάνιση sites με κωδικό 000 (Connection Error):')
        st.table(df[df.status_code == '000'])

    if len(df[df.status_code == '-']) > 0:
        st.header('Εμφάνιση sites χωρίς κωδικό (Read timed out):')
        st.table(df[df.status_code == '-'])

    if len(df[df.status_code.isin([i for i in range(400, 500)])]) > 0:
        st.header('Εμφάνιση sites με κωδικό 4xx (client errors):')
        st.table(df[df.status_code.isin([i for i in range(400, 500)])])

    if len(df[df.status_code.isin([i for i in range(300, 400)])]) > 0:
        st.header('Εμφάνιση sites με κωδικό 3xx (redirection) :')
        st.table(df[df.status_code.isin([i for i in range(300, 400)])])

    if len(df[df.status_code.isin([i for i in range(200, 300)])]) > 0:
        st.header('Εμφάνιση sites με κωδικό 2xx (success) :')
        st.table(df[df.status_code.isin([i for i in range(200, 300)])])

    timezone = pytz.timezone('Europe/Athens')
    now = datetime.now(tz=timezone)  # current date and time
    date_time = now.strftime("%d_%m_%y-%H:%M- ")

    tmp_download_link = download_link(data, date_time + 'urls_in_army_domain.csv',
                                      'Κάντε κλικ για να κατεβάσετε τα δεδομένα σε csv μορφή!')
    st.markdown(tmp_download_link, unsafe_allow_html=True)
