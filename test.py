# -*- coding: utf-8 -*-
"""
Ulitka.uz WooCommerce do'konini to'liq kezadigan parser:
- https://ulitka.uz/shop/ sahifasidan mahsulot URL'larini oladi (pagination bilan)
- Har bir mahsulot sahifasiga kirib, batafsil ma'lumotlarni dict ko'rinishida yig'adi
- Natija: List[Dict]

Talab:
  pip install requests beautifulsoup4

Oddiy ishlatish:
  from ulitka_crawler import crawl_all_products
  items = crawl_all_products()
  print(items[0])
"""

import json
import re
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://ulitka.uz"
SHOP_URL = f"{BASE_URL}/shop/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36",
    "Accept-Language": "ru,en;q=0.9,uz;q=0.8",
}


def _text(el) -> str:
    return el.get_text(" ", strip=True) if el else ""


def _to_int_price(price_text: str) -> Optional[int]:
    if not price_text:
        return None
    cleaned = price_text.replace("\xa0", " ").strip()
    digits = re.findall(r"\d+", cleaned)
    return int("".join(digits)) if digits else None


def _parse_json_ld(soup: BeautifulSoup) -> Dict[str, Any]:
    """
    Sahifadagi JSON-LD (schema.org) dan Product obyektini ajratib olish.
    """
    product_ld: Dict[str, Any] = {}
    for sc in soup.find_all("script", {"type": "application/ld+json"}):
        try:
            raw = sc.string or ""
            # Ba'zi saytlar bir nechta JSON obyektni ketma-ket qo'yadi — buni qo'llab-quvvatlash:
            data = json.loads(raw)
        except Exception:
            continue

        candidates: List[Dict[str, Any]] = []
        if isinstance(data, dict) and data.get("@type") == "Product":
            candidates.append(data)
        if isinstance(data, dict) and isinstance(data.get("@graph"), list):
            for item in data["@graph"]:
                if isinstance(item, dict) and item.get("@type") == "Product":
                    candidates.append(item)

        if candidates:
            product_ld = candidates[0]
            break
    return product_ld


def parse_shop_list(html: str) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """
    Shop sahifasidan mahsulot kartalari va keyingi sahifa linkini qaytaradi.
    """
    soup = BeautifulSoup(html, "html.parser")
    items: List[Dict[str, Any]] = []

    for li in soup.select("ul.products li.product"):
        url = ""
        a = li.select_one("a.woocommerce-LoopProduct-link.woocommerce-loop-product__link")
        if a and a.get("href"):
            url = a["href"].strip()

        title = _text(li.select_one("h2.woocommerce-loop-product__title"))
        price_text = _text(li.select_one(".price .woocommerce-Price-amount.amount")).replace("\xa0", " ")
        currency = _text(li.select_one(".price .woocommerce-Price-amount.amount .woocommerce-Price-currencySymbol"))
        price = _to_int_price(price_text)
        cats = [a.get_text(strip=True) for a in li.select(".archive-product-categories a")]
        img = li.select_one(".archive-img-wrap img")
        image_url = img.get("src", "").strip() if img else ""

        items.append(
            {
                "list_title": title,
                "list_url": url,
                "list_price": price,
                "list_currency": currency,
                "list_price_text": price_text,
                "list_categories": cats,
                "list_image": image_url,
            }
        )

    # Keyingi sahifa
    next_link = None
    nav = soup.select_one("nav.woocommerce-pagination")
    if nav:
        a_next = nav.select_one("a.next.page-numbers")
        if a_next and a_next.get("href"):
            next_link = a_next["href"].strip()
        else:
            # Agar "next" bo'lmasa, eng katta raqamni topib, currentdan keyingi sahifa yo'qligini bildiramiz
            next_link = None

    return items, next_link


def parse_product_detail(html: str) -> Dict[str, Any]:
    """
    Bitta product detail sahifasidan boy ma'lumotlarni dict ko'rinishida qaytaradi.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Asosiy konteyner va ID
    container = soup.select_one("div.product.type-product")
    html_id = container.get("id", "") if container else ""
    html_product_id = re.search(r"product-(\d+)", html_id)
    product_id_from_html = html_product_id.group(1) if html_product_id else None

    # H1 sarlavha
    title = _text(soup.select_one("h1.product_title.entry-title"))

    # Narx va valyuta
    amount_el = soup.select_one("p.price .woocommerce-Price-amount.amount")
    currency_el = soup.select_one("p.price .woocommerce-Price-amount.amount .woocommerce-Price-currencySymbol")
    price_text = _text(amount_el).replace("\xa0", " ")
    currency = _text(currency_el)
    price = _to_int_price(price_text)

    # Kategoriya(lar)
    cats = [a.get_text(strip=True) for a in soup.select(".product_meta .posted_in a[rel='tag']")]

    # Breadcrumbs
    breadcrumb_links = [a.get_text(strip=True) for a in soup.select(".woo-breadcrumbs a")]
    breadcrumbs = breadcrumb_links + (
        [title] if title and (not breadcrumb_links or breadcrumb_links[-1] != title) else []
    )

    # Tavsiflar
    short_desc = _text(soup.select_one(".woocommerce-product-details__short-description"))
    long_desc = _text(soup.select_one("#tab-description"))

    # Rasmlar
    image_urls: List[str] = []
    seen = set()
    for img in soup.select(".woocommerce-product-gallery__image img"):
        for key in ("data-large_image", "data-src", "src"):
            url = (img.get(key) or "").strip()
            if url and url not in seen:
                seen.add(url)
                image_urls.append(url)
        a = img.find_parent("a")
        if a and a.get("href"):
            url = a["href"].strip()
            if url and url not in seen:
                seen.add(url)
                image_urls.append(url)
        srcset = (img.get("srcset") or "").strip()
        if srcset:
            for token in srcset.split(","):
                u = token.strip().split(" ")[0]
                if u and u not in seen:
                    seen.add(u)
                    image_urls.append(u)

    # Canonical
    canonical = ""
    link_canon = soup.find("link", rel="canonical")
    if link_canon and link_canon.get("href"):
        canonical = link_canon["href"].strip()

    # Add to cart
    form = soup.select_one("form.cart")
    add_to_cart_action = form.get("action", "").strip() if form else ""
    add_to_cart_method = (form.get("method", "") or "").strip().lower() if form else ""
    add_to_cart_id = None
    if form:
        atc = form.select_one('[name="add-to-cart"]')
        if atc and atc.get("value"):
            add_to_cart_id = atc["value"].strip()

    # Related products
    related: List[Dict[str, Any]] = []
    for li in soup.select("section.related li.product"):
        r_title = _text(li.select_one("h2.woocommerce-loop-product__title"))
        r_link = ""
        a = li.select_one("a.woocommerce-LoopProduct-link.woocommerce-loop-product__link")
        if a and a.get("href"):
            r_link = a["href"].strip()
        r_amount = _text(li.select_one(".price .woocommerce-Price-amount.amount")).replace("\xa0", " ")
        r_currency = _text(li.select_one(".price .woocommerce-Price-amount.amount .woocommerce-Price-currencySymbol"))
        related.append(
            {
                "title": r_title,
                "url": r_link,
                "price": _to_int_price(r_amount),
                "currency": r_currency,
                "price_text": r_amount,
            }
        )

    # JSON-LD
    ld = _parse_json_ld(soup)
    ld_sku = str(ld.get("sku")) if isinstance(ld.get("sku"), (int, str)) else None
    ld_offers = ld.get("offers") or []
    if isinstance(ld_offers, dict):
        ld_offers = [ld_offers]
    availability = None
    price_valid_until = None
    seller_name = None
    if ld_offers:
        o = ld_offers[0]
        availability = o.get("availability")
        price_valid_until = o.get("priceValidUntil")
        seller = o.get("seller") or {}
        if isinstance(seller, dict):
            seller_name = seller.get("name")

    data: Dict[str, Any] = {
        "id": add_to_cart_id or product_id_from_html or ld_sku,
        "sku": ld_sku,
        "title": title,
        "url": canonical,
        "price": price,
        "currency": currency,
        "price_text": price_text,
        "availability": availability,
        "price_valid_until": price_valid_until,
        "seller_name": seller_name,
        "category": cats[0] if cats else None,
        "categories": cats,
        "breadcrumbs": breadcrumbs,
        "description_short": short_desc,
        "description": long_desc,
        "images": image_urls,
        "add_to_cart": {
            "product_id": add_to_cart_id,
            "action": add_to_cart_action,
            "method": add_to_cart_method,
        },
        "html_container_id": html_id,
        "related_products": related,
    }
    return data


def fetch(session: requests.Session, url: str, *, timeout: float = 15.0) -> Optional[str]:
    try:
        resp = session.get(url, headers=HEADERS, timeout=timeout)
        if resp.status_code == 200 and "text/html" in resp.headers.get("Content-Type", ""):
            return resp.text
        # WooCommerce pagination 404 bo'lishi mumkin
        if resp.status_code == 404:
            return None
        # 200 lekin html bo'lmasa ham None qaytarib qo'yamiz
        return None
    except requests.RequestException:
        return None


def crawl_all_products(
    base_shop_url: str = SHOP_URL,
    *,
    delay_sec: float = 0.7,
    max_pages: Optional[int] = None,
    include_list_summary: bool = True,
) -> List[Dict[str, Any]]:
    """
    Barcha sahifalarni kezib, mahsulot detallarini qaytaradi.

    Parametrlar:
      base_shop_url: do'kon vitrina URL
      delay_sec: so'rovlar orasidagi pauza (sekund)
      max_pages: cheklash uchun (None bo'lsa, iloji boricha ko'p)
      include_list_summary: list sahifasidagi qisqa ma'lumotni detalga biriktirish

    Natija: List[Dict]
    """
    session = requests.Session()
    seen_urls = set()
    results: List[Dict[str, Any]] = []

    # Birinchi sahifa
    next_url = base_shop_url
    page_count = 0

    while next_url:
        page_count += 1
        if max_pages and page_count > max_pages:
            break

        html = fetch(session, next_url)
        if not html:
            break

        list_items, link_next = parse_shop_list(html)

        # Detallarni yig'ish
        for it in list_items:
            prod_url = it.get("list_url") or ""
            if not prod_url:
                continue
            full_url = urljoin(BASE_URL, prod_url)
            if full_url in seen_urls:
                continue
            seen_urls.add(full_url)

            time.sleep(delay_sec)
            detail_html = fetch(session, full_url)
            if not detail_html:
                continue
            detail = parse_product_detail(detail_html)

            if include_list_summary:
                detail["list_summary"] = it

            # Agar canonical bo'sh bo'lsa, baribir kirilgan URL'ni saqlab qo'yamiz
            if not detail.get("url"):
                detail["url"] = full_url

            results.append(detail)

        # Keyingi sahifaga o'tish
        if link_next:
            next_url = urljoin(BASE_URL, link_next)
        else:
            # Agar pagination link yo'q bo'lsa, to'xtaymiz
            break

        time.sleep(delay_sec)

    return results


# Namuna: modul sifatida import qilinmasa va to'g'ridan-to'g'ri ishga tushirilsa
if __name__ == "__main__":
    data = crawl_all_products()  # barcha sahifalar
    # JSON ko'rinishida ko'rsatamiz
    with open("products.json", "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
