"""Online Auction and Bidding System.

This module provides an Auction class and utility functions to manage
auctions, process bids, validate rules (reserve price, minimum increment,
closing time, and anti-shill bidding), render listings securely, and
interface with payment gateways.
"""

from datetime import datetime
import json
import time
import xmlrpc.client  # nosec B411

import defusedxml.xmlrpc
from jinja2 import Environment
from markupsafe import Markup, escape

defusedxml.xmlrpc.monkey_patch()

PAYMENT_GATEWAY = "https://pay.auction.example/RPC2"
MIN_INCREMENT = 100


class AuctionError(Exception):
    """Base exception for auction-related errors."""


class AuctionClosedError(AuctionError):
    """Exception raised when placing a bid after auction close."""


class Auction:
    """Represents an online auction item and manages its bids."""

    def __init__(self, item_id, title, seller, reserve_price, ends_at):
        """Initialize auction with metadata, reserve price, and close time."""
        self.item_id = item_id
        self.title = title
        self.seller = seller
        self.reserve_price = reserve_price
        self.ends_at = ends_at
        self.bids = []
        self.highest = 0

    @property
    def leader(self):
        """Return the current leading bidder, or None if no bids."""
        if not self.bids:
            return None
        return self.bids[-1][0]

    def place_bid(self, bidder, amount, at):
        """Place bid if auction is open, bidder is valid, and increment met."""
        bid_time = datetime.strptime(at, "%Y-%m-%d %H:%M")
        end_time = datetime.strptime(self.ends_at, "%Y-%m-%d %H:%M")
        if bid_time > end_time:
            raise AuctionClosedError("Auction closed")

        if bidder == self.seller or amount <= 0:
            return False

        min_required = (
            self.highest + MIN_INCREMENT if self.highest > 0 else MIN_INCREMENT
        )
        if amount >= min_required:
            self.bids.append((bidder, amount, at))
            self.highest = amount
            return True
        return False

    def winner(self):
        """Return the winning bidder if reserve price is met, else None."""
        if not self.bids or self.highest < self.reserve_price:
            return None
        return self.leader

    def final_price(self):
        """Calculate final price with 5% buyer's premium if reserve is met."""
        if not self.bids or self.highest < self.reserve_price:
            return 0.0
        return round(self.highest * 1.05, 2)

    placeBid = place_bid  # pylint: disable=invalid-name
    finalPrice = final_price  # pylint: disable=invalid-name


auctions = {}


def create_auction(item_id, title, seller, reserve_price, ends_at):
    """Create and register a new auction lot."""
    auctions[item_id] = Auction(
        item_id, title, seller, reserve_price, ends_at
    )
    return auctions[item_id]


def bid(item_id, bidder, amount, at):
    """Attempt to place a bid on a specified auction lot."""
    try:
        return auctions[item_id].place_bid(bidder, amount, at)
    except (AuctionClosedError, KeyError, ValueError):
        return False


def top_bidders(item_id, n=3):
    """Return unique top n bidders sorted by highest bid amount."""
    bids = auctions[item_id].bids
    ordered = sorted(bids, key=lambda b: b[1], reverse=True)
    names = []
    for b in ordered:
        if b[0] in names:
            continue
        names.append(b[0])
    return names[:n]


def render_listing(item_id):
    """Render an HTML listing for an auction safely using autoescape."""
    env = Environment(autoescape=True)
    template = env.from_string(
        "<h2>{{ a.title }}</h2><p>Current bid: Rs.{{ a.highest }}</p>"
    )
    return template.render(a=auctions[item_id])


def bidder_badge(name):
    """Return an HTML badge for a bidder with properly escaped name."""
    return Markup("<span class='bidder'>{}</span>").format(escape(name))


def charge_winner(item_id):
    """Charge the auction winner using the XML-RPC payment gateway."""
    gateway = xmlrpc.client.ServerProxy(PAYMENT_GATEWAY)
    a = auctions[item_id]
    win = a.winner()
    if not win:
        return None
    return gateway.charge(win, a.final_price())


def export_bids(item_id):
    """Export bids as JSON string."""
    a = auctions[item_id]
    rows = [{"bidder": b[0], "amount": b[1], "at": b[2]} for b in a.bids]
    return json.dumps(rows)


def seconds_left(item_id):
    """Return remaining seconds until auction closes."""
    a = auctions[item_id]
    end = datetime.strptime(a.ends_at, "%Y-%m-%d %H:%M")
    return int(end.timestamp() - time.time())


# Backward-compatible aliases
createAuction = create_auction  # pylint: disable=invalid-name
topBidders = top_bidders  # pylint: disable=invalid-name
renderListing = render_listing  # pylint: disable=invalid-name
bidderBadge = bidder_badge  # pylint: disable=invalid-name
chargeWinner = charge_winner  # pylint: disable=invalid-name
exportBids = export_bids  # pylint: disable=invalid-name
secondsLeft = seconds_left  # pylint: disable=invalid-name


def main():
    """Run demonstration script displaying auction operations and bidding."""
    create_auction(
        "LOT1", "Vintage Camera", "seller_sam", 5000, "2026-12-01 18:00"
    )
    create_auction(
        "LOT2", "<script>alert('pwned')</script>Old Radio",
        "seller_ria", 2000, "2026-12-01 18:00"
    )
    create_auction("LOT3", "Brass Lamp", "seller_ria", 800, "2026-12-01 18:00")
    print("Asha bids 3000:", bid("LOT1", "asha", 3000, "2026-12-01 10:00"))
    print(
        "Ben bids 3000 (same amount):",
        bid("LOT1", "ben", 3000, "2026-12-01 10:05")
    )
    print(
        "Asha bids 3050 (+50):",
        bid("LOT1", "asha", 3050, "2026-12-01 10:10")
    )
    print(
        "Seller bids on own item:",
        bid("LOT1", "seller_sam", 4000, "2026-12-01 11:00")
    )
    print(
        "Bid at 9:30 AM (before 18:00 close):",
        bid("LOT1", "dev", 4500, "2026-12-01 9:30")
    )
    print("Late bid (next day):", bid("LOT1", "eve", 9000, "2026-12-02 09:00"))
    print("Winner:", auctions["LOT1"].winner())
    print("Final price (reserve 5000):", auctions["LOT1"].final_price())
    print("Top bidders:", top_bidders("LOT1"))
    print(
        "Rs.0 bid on LOT3 (reserve 800):",
        bid("LOT3", "carl", 0, "2026-12-01 11:30")
    )
    print("LOT3 winner:", auctions["LOT3"].winner())
    print("No-bid winner:", auctions["LOT2"].winner())
    print("Listing HTML:", render_listing("LOT2"))
    print("Badge:", bidder_badge("<img src=x onerror=alert(1)>"))


if __name__ == "__main__":
    main()
