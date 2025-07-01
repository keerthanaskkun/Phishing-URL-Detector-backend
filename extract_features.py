import re
import socket
import tldextract
import urllib
from urllib.parse import urlparse

def extract_features(url):
    features = []

    # Extract components
    parsed = urlparse(url)
    ext = tldextract.extract(url)
    domain = ext.domain + '.' + ext.suffix
    hostname = parsed.hostname or ''
    path = parsed.path or ''

    def count_digits(s): return sum(c.isdigit() for c in s)
    def safe_div(a, b): return a / b if b else 0

    # Basic counts
    features.append(len(url))  # length_url
    features.append(len(hostname))  # length_hostname
    features.append(1 if re.match(r'http[s]?://\d+\.\d+\.\d+\.\d+', url) else 0)  # ip
    features.append(url.count('.'))  # nb_dots
    features.append(url.count('-'))  # nb_hyphens
    features.append(url.count('@'))  # nb_at
    features.append(url.count('?'))  # nb_qm
    features.append(url.count('&'))  # nb_and
    features.append(url.count('|'))  # nb_or
    features.append(url.count('='))  # nb_eq
    features.append(url.count('_'))  # nb_underscore
    features.append(url.count('~'))  # nb_tilde
    features.append(url.count('%'))  # nb_percent
    features.append(url.count('/'))  # nb_slash
    features.append(url.count('*'))  # nb_star
    features.append(url.count(':'))  # nb_colon
    features.append(url.count(','))  # nb_comma
    features.append(url.count(';'))  # nb_semicolumn
    features.append(url.count('$'))  # nb_dollar
    features.append(url.count(' '))  # nb_space
    features.append(1 if 'www' in url else 0)  # nb_www
    features.append(1 if '.com' in url else 0)  # nb_com
    features.append(url.count('//'))  # nb_dslash

    # Advanced
    features.append(1 if 'http' in path else 0)  # http_in_path
    features.append(1 if 'http' in url and 'https' in url else 0)  # https_token
    features.append(safe_div(count_digits(url), len(url)))  # ratio_digits_url
    features.append(safe_div(count_digits(hostname), len(hostname)))  # ratio_digits_host
    features.append(1 if 'xn--' in url else 0)  # punycode
    features.append(1 if ':' in parsed.netloc.split(':')[-1] else 0)  # port
    features.append(1 if ext.suffix in path else 0)  # tld_in_path
    features.append(1 if ext.suffix in ext.subdomain else 0)  # tld_in_subdomain
    features.append(1 if ext.subdomain and ext.domain not in ext.subdomain else 0)  # abnormal_subdomain
    features.append(len(ext.subdomain.split('.')) if ext.subdomain else 0)  # nb_subdomains
    features.append(1 if '-' in ext.domain else 0)  # prefix_suffix
    features.append(1 if re.search(r'rand|temp|test|demo', domain) else 0)  # random_domain
    features.append(1 if re.search(r'bit\.ly|goo\.gl|tinyurl\.com|ow\.ly', url) else 0)  # shortening_service
    features.append(1 if '.' in path.split('/')[-1] else 0)  # path_extension
    features.append(url.count('//') - 1)  # nb_redirection
    features.append(1 if re.match(r'^https?://(?!'+hostname+')', url) else 0)  # nb_external_redirection

    # Word length features
    words = re.findall(r'[a-zA-Z0-9]+', url)
    words_host = hostname.split('.')
    words_path = path.split('/')

    features.append(len(''.join(words)))  # length_words_raw
    features.append(1 if re.search(r'(.)\1\1', url) else 0)  # char_repeat
    features.append(min([len(w) for w in words]) if words else 0)  # shortest_words_raw
    features.append(min([len(w) for w in words_host]) if words_host else 0)  # shortest_word_host
    features.append(min([len(w) for w in words_path]) if words_path else 0)  # shortest_word_path
    features.append(max([len(w) for w in words]) if words else 0)  # longest_words_raw
    features.append(max([len(w) for w in words_host]) if words_host else 0)  # longest_word_host
    features.append(max([len(w) for w in words_path]) if words_path else 0)  # longest_word_path
    features.append(safe_div(sum([len(w) for w in words]), len(words)))  # avg_words_raw
    features.append(safe_div(sum([len(w) for w in words_host]), len(words_host)))  # avg_word_host
    features.append(safe_div(sum([len(w) for w in words_path]), len(words_path)))  # avg_word_path

    # Dummy values for ML-only features (to keep length = 87)
    features += [0] * (87 - len(features))  # Fill remaining features with 0

    return features
