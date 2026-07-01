#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knowledge_updater.py — Self-improving knowledge crawler for Omnichannel CX Optimizer.

This pipeline continuously expands the SECOND-KNOWLEDGE-BRAIN.md with cutting-edge
research and industry insights on omnichannel customer experience optimization.

Pipeline Architecture:
    1. Source Discovery → ArXiv, industry blogs, academic repositories
    2. Content Extraction → crawl4ai for web scraping, arXiv API for papers
    3. Semantic Scoring → Recency-weighted relevance ranking
    4. Intelligent Deduplication → SHA-256 hash-based duplicate prevention
    5. Structured Appending → Formatted entries with metadata and citations

Execution: Scheduled weekly via cron. Manual execution: python tools/knowledge_updater.py

Dependencies:
    pip install crawl4ai requests beautifulsoup4

Author: Omnichannel CX Optimizer Skill
Version: 1.0.0
License: MIT
"""

from __future__ import annotations

import abc
import dataclasses
import hashlib
import json
import logging
import os
import re
import sys
import tempfile
import typing
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(
            Path(__file__).parent.parent / "logs" / "knowledge_updater.log",
            encoding="utf-8",
        )
        if (Path(__file__).parent.parent / "logs").exists()
        else logging.NullHandler(),
    ],
)
logger = logging.getLogger("knowledge_updater")

# =============================================================================
# CONSTANTS & CONFIGURATION
# =============================================================================

SKILL_ID = 106
SKILL_SLUG = "omnichannel-cx-optimizer"
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
BRAIN_PATH = PROJECT_ROOT / "SECOND-KNOWLEDGE-BRAIN.md"
CACHE_PATH = PROJECT_ROOT / ".cache" / "knowledge_cache.json"
LOGS_PATH = PROJECT_ROOT / "logs"

# ArXiv configuration for CS.HC (Human-Computer Interaction) papers
ARXIV_CATEGORIES = ["cs.HC", "cs.CY", "cs.SI"]
ARXIV_BASE_URL = "http://export.arxiv.org/api/query"

# Domain-specific search queries for targeted research
SEARCH_QUERIES = [
    "omnichannel customer journey mapping",
    "service blueprint customer experience",
    "customer experience metrics NPS CES",
    "cross-channel continuity CX",
    "omnichannel friction analysis",
    "customer touchpoint optimization",
    "CX measurement maturity",
    "emotional peak-end design",
]

# Authoritative sources for continuous monitoring
SOURCE_CONFIGS = [
    {
        "name": "Nielsen Norman Group",
        "base_url": "https://www.nngroup.com",
        "search_paths": ["/articles/", "/topics/ux-customer-experience/"],
        "content_selectors": ["article", ".entry-content", ".post-content"],
    },
    {
        "name": "Forrester CX Research",
        "base_url": "https://www.forrester.com",
        "search_paths": ["/data/category/customer-experience/"],
        "content_selectors": ["article", ".report-content"],
    },
    {
        "name": "Qualtrics XM Institute",
        "base_url": "https://www.qualtrics.com",
        "search_paths": ["/experience-management/customer/"],
        "content_selectors": ["article", ".blog-content", ".resource-content"],
    },
    {
        "name": "Harvard Business Review",
        "base_url": "https://hbr.org",
        "search_paths": ["/topic/customer-experience"],
        "content_selectors": ["article", ".article-body", ".post-content"],
    },
]

# Domain keywords for relevance scoring
DOMAIN_KEYWORDS = [
    "omnichannel",
    "customer journey",
    "service blueprint",
    "CX metrics",
    "NPS",
    "CES",
    "CSAT",
    "customer experience",
    "touchpoint",
    "cross-channel",
    "friction",
    "personalization",
    "customer effort score",
    "measurement maturity",
    "peak-end rule",
    "service recovery",
    "channel parity",
    "identity stitching",
    "emotional design",
]

# Evidence hierarchy weights
EVIDENCE_HIERARCHY = {
    "systematic_review": 1.0,
    "meta_analysis": 0.95,
    "rct": 0.9,
    "benchmark": 0.85,
    "cohort_study": 0.75,
    "case_study": 0.65,
    "expert_opinion": 0.5,
    "blog": 0.3,
}


# =============================================================================
# DATA MODELS
# =============================================================================


@dataclasses.dataclass(frozen=True)
class KnowledgeEntry:
    """Immutable knowledge entry with complete metadata."""

    title: str
    url: str
    authors: str
    year: int
    abstract: str
    venue: str = ""
    doi: str = ""
    evidence_type: str = "unknown"
    relevance_score: float = 0.0
    extracted_date: date = dataclasses.field(default_factory=date.today)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "title": self.title,
            "url": self.url,
            "authors": self.authors,
            "year": self.year,
            "abstract": self.abstract,
            "venue": self.venue,
            "doi": self.doi,
            "evidence_type": self.evidence_type,
            "relevance_score": self.relevance_score,
            "extracted_date": self.extracted_date.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "KnowledgeEntry":
        """Create instance from dictionary."""
        return cls(
            title=data["title"],
            url=data["url"],
            authors=data["authors"],
            year=data["year"],
            abstract=data["abstract"],
            venue=data.get("venue", ""),
            doi=data.get("doi", ""),
            evidence_type=data.get("evidence_type", "unknown"),
            relevance_score=data.get("relevance_score", 0.0),
            extracted_date=date.fromisoformat(data.get("extracted_date", date.today().isoformat())),
        )


@dataclasses.dataclass
class CrawlerStats:
    """Statistics for crawler execution tracking."""

    total_fetched: int = 0
    unique_entries: int = 0
    duplicates_skipped: int = 0
    failed_sources: List[str] = dataclasses.field(default_factory=list)
    execution_time_seconds: float = 0.0

    def to_summary(self) -> str:
        """Generate human-readable summary."""
        return f"""
Crawler Execution Summary:
  Total entries fetched: {self.total_fetched}
  Unique entries added: {self.unique_entries}
  Duplicates skipped: {self.duplicates_skipped}
  Failed sources: {len(self.failed_sources)}
  Execution time: {self.execution_time_seconds:.2f} seconds
""".strip()


# =============================================================================
# ABSTRACT BASE CLASSES
# =============================================================================


class SourceFetcher(abc.ABC):
    """Abstract base for knowledge source fetchers."""

    @abc.abstractmethod
    def fetch(self) -> List[KnowledgeEntry]:
        """Fetch knowledge entries from the source."""
        pass

    @abc.abstractmethod
    def source_name(self) -> str:
        """Return human-readable source name."""
        pass


# =============================================================================
# CORE FUNCTIONS
# =============================================================================


def compute_url_hash(url: str) -> str:
    """Generate deterministic SHA-256 hash for URL/DOI deduplication.

    Args:
        url: The URL or DOI string to hash.

    Returns:
        First 16 characters of hexadecimal SHA-256 hash.
    """
    return hashlib.sha256(url.encode("utf-8", errors="ignore")).hexdigest()[:16]


def load_seen_hashes() -> Set[str]:
    """Load all existing URL hashes from SECOND-KNOWLEDGE-BRAIN.md.

    Returns:
        Set of 16-character hexadecimal hashes already present.
    """
    if not BRAIN_PATH.exists():
        logger.warning(f"Knowledge brain not found at {BRAIN_PATH}")
        return set()

    try:
        content = BRAIN_PATH.read_text(encoding="utf-8")
        hashes = set(re.findall(r"<!--hash:([0-9a-f]{16})-->", content))
        logger.info(f"Loaded {len(hashes)} existing hashes from knowledge base")
        return hashes
    except Exception as e:
        logger.error(f"Failed to read knowledge base: {e}")
        return set()


def compute_relevance_score(entry: KnowledgeEntry) -> float:
    """Compute relevance score combining recency and domain keyword matching.

    Formula: recency_weight * (0.4 + 0.6 * keyword_match_ratio)

    Args:
        entry: The knowledge entry to score.

    Returns:
        Float between 0.0 and 1.0 representing relevance.
    """
    # Recency scoring: newer is better, decays over 8 years
    current_year = date.today().year
    years_old = current_year - entry.year
    recency = max(0.0, 1.0 - (years_old / 8.0)) if entry.year > 1900 else 0.3

    # Keyword matching: count domain keywords in title + abstract
    searchable_text = f"{entry.title} {entry.abstract}".lower()
    keyword_hits = sum(1 for kw in DOMAIN_KEYWORDS if kw.lower() in searchable_text)
    keyword_ratio = min(1.0, keyword_hits / max(1, len(DOMAIN_KEYWORDS) * 0.15))

    # Apply evidence hierarchy bonus
    evidence_bonus = EVIDENCE_HIERARCHY.get(entry.evidence_type, 0.5)

    score = round(recency * (0.3 + 0.5 * keyword_ratio + 0.2 * evidence_bonus), 3)
    return max(0.0, min(1.0, score))


def infer_evidence_type(entry: KnowledgeEntry) -> str:
    """Infer evidence type from venue and metadata.

    Args:
        entry: The knowledge entry to classify.

    Returns:
        Evidence type key from EVIDENCE_HIERARCHY.
    """
    venue_lower = entry.venue.lower()
    url_lower = entry.url.lower()

    if "systematic review" in venue_lower or "systematic" in url_lower:
        return "systematic_review"
    if "meta-analysis" in venue_lower or "meta" in url_lower:
        return "meta_analysis"
    if "arxiv" in url_lower:
        return "cohort_study"
    if "hbr.org" in url_lower or "forrester" in url_lower:
        return "expert_opinion"
    if "blog" in url_lower or "/blog/" in url_lower:
        return "blog"
    if "nngroup.com" in url_lower:
        return "expert_opinion"

    return "expert_opinion"


def format_entry_block(entry: KnowledgeEntry) -> str:
    """Format a knowledge entry as a markdown block for SECOND-KNOWLEDGE-BRAIN.md.

    Args:
        entry: The knowledge entry to format.

    Returns:
        Formatted markdown string.
    """
    hash_val = compute_url_hash(entry.url)
    today = date.today().isoformat()

    block = f"""### [{today}] {entry.title}
- **Authors:** {entry.authors or 'n/a'}
- **Year:** {entry.year}
- **Venue:** {entry.venue or 'n/a'}
- **Link:** {entry.url}
- **DOI:** {entry.doi or 'n/a'}
- **Evidence Type:** {entry.evidence_type}
- **Relevance Score:** {entry.relevance_score:.3f}
- **Key Findings:** {(entry.abstract or '(abstract pending)')[:400]}...
<!--hash:{hash_val}-->"""

    return block


# =============================================================================
# ARXIV FETCHER
# =============================================================================


class ArxivFetcher(SourceFetcher):
    """Fetch recent papers from arXiv using the ArXiv API."""

    def __init__(self, categories: List[str], max_results: int = 50):
        """Initialize with categories and result limit.

        Args:
            categories: List of arXiv category codes (e.g., ['cs.HC']).
            max_results: Maximum papers to fetch per category.
        """
        self.categories = categories
        self.max_results = max_results
        self.entries: List[KnowledgeEntry] = []

    def source_name(self) -> str:
        return "ArXiv"

    def fetch(self) -> List[KnowledgeEntry]:
        """Fetch recent papers from configured arXiv categories.

        Returns:
            List of KnowledgeEntry objects from arXiv.
        """
        import urllib.parse
        import urllib.request
        import xml.etree.ElementTree as ET

        all_entries = []

        for category in self.categories:
            try:
                # Build query for recent papers in category
                query = f"cat:{category}"
                search_url = f"{ARXIV_BASE_URL}?search_query={urllib.parse.quote(query)}&start=0&max_results={self.max_results}&sortBy=submittedDate&sortOrder=descending"

                logger.info(f"Fetching arXiv papers for category: {category}")
                with urllib.request.urlopen(search_url, timeout=30) as response:
                    xml_data = response.read().decode("utf-8")

                # Parse XML response
                root = ET.fromstring(xml_data)
                entries = self._parse_arxiv_response(root)
                all_entries.extend(entries)
                logger.info(f"Retrieved {len(entries)} papers from {category}")

            except Exception as e:
                logger.error(f"Failed to fetch arXiv category {category}: {e}")

        return all_entries

    def _parse_arxiv_response(self, root: ET.Element) -> List[KnowledgeEntry]:
        """Parse arXiv API XML response into KnowledgeEntry objects.

        Args:
            root: XML root element from arXiv API response.

        Returns:
            List of KnowledgeEntry objects.
        """
        entries = []
        ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

        for entry in root.findall("atom:entry", ns):
            try:
                # Extract paper metadata
                title = entry.find("atom:title", ns)
                title_text = title.text.strip().replace("\n", " ") if title is not None else "Untitled"

                # Get arXiv ID for URL construction
                id_elem = entry.find("atom:id", ns)
                arxiv_id = id_elem.text.split("/abs/")[-1] if id_elem is not None else ""
                url = f"https://arxiv.org/abs/{arxiv_id}"

                # Extract authors
                authors = []
                for author in entry.findall("atom:author", ns):
                    name_elem = author.find("atom:name", ns)
                    if name_elem is not None:
                        authors.append(name_elem.text)
                authors_text = ", ".join(authors) if authors else "Unknown"

                # Extract year from published date
                published = entry.find("atom:published", ns)
                year = int(published.text[:4]) if published is not None else date.today().year

                # Extract abstract
                summary = entry.find("atom:summary", ns)
                abstract = summary.text.strip().replace("\n", " ") if summary is not None else ""

                # Create knowledge entry
                knowledge_entry = KnowledgeEntry(
                    title=title_text,
                    url=url,
                    authors=authors_text,
                    year=year,
                    abstract=abstract[:800],
                    venue="arXiv preprint",
                    doi=f"arXiv:{arxiv_id}",
                    evidence_type="cohort_study",
                )

                entries.append(knowledge_entry)

            except Exception as e:
                logger.warning(f"Failed to parse arXiv entry: {e}")
                continue

        return entries


# =============================================================================
# WEB CRAWLER FETCHER
# =============================================================================


class WebCrawlerFetcher(SourceFetcher):
    """Fetch content from web sources using crawl4ai."""

    def __init__(self, source_configs: List[Dict[str, Any]]):
        """Initialize with source configurations.

        Args:
            source_configs: List of source configuration dictionaries.
        """
        self.source_configs = source_configs
        self.entries: List[KnowledgeEntry] = []

    def source_name(self) -> str:
        return "WebCrawler"

    def fetch(self) -> List[KnowledgeEntry]:
        """Crawl configured web sources for relevant content.

        Returns:
            List of KnowledgeEntry objects from web sources.
        """
        all_entries = []

        for config in self.source_configs:
            try:
                entries = self._crawl_source(config)
                all_entries.extend(entries)
                logger.info(f"Retrieved {len(entries)} entries from {config['name']}")
            except Exception as e:
                logger.error(f"Failed to crawl {config['name']}: {e}")

        return all_entries

    def _crawl_source(self, config: Dict[str, Any]) -> List[KnowledgeEntry]:
        """Crawl a single configured source.

        Args:
            config: Source configuration dictionary.

        Returns:
            List of KnowledgeEntry objects from this source.
        """
        entries = []
        base_url = config["base_url"]
        source_name = config["name"]

        try:
            # Attempt to import crawl4ai
            from crawl4ai import WebCrawler

            crawler = WebCrawler(verbose=False)
            crawler.warmup()

            # Crawl main page and search paths
            urls_to_crawl = [base_url] + [
                base_url.rstrip("/") + path for path in config.get("search_paths", [])
            ]

            for url in urls_to_crawl:
                try:
                    result = crawler.run(url=url)
                    if result.success:
                        entry = self._parse_crawl_result(result, source_name, url)
                        if entry:
                            entries.append(entry)
                except Exception as e:
                    logger.warning(f"Failed to crawl {url}: {e}")

        except ImportError:
            logger.warning("crawl4ai not installed; skipping web crawling")
        except Exception as e:
            logger.error(f"Web crawling failed for {source_name}: {e}")

        return entries

    def _parse_crawl_result(
        self, result: Any, source_name: str, url: str
    ) -> Optional[KnowledgeEntry]:
        """Parse crawl4ai result into KnowledgeEntry.

        Args:
            result: crawl4ai result object.
            source_name: Human-readable source name.
            url: URL that was crawled.

        Returns:
            KnowledgeEntry or None if parsing fails.
        """
        try:
            markdown = getattr(result, "markdown", "")
            if not markdown:
                return None

            # Extract first paragraph as abstract
            paragraphs = re.split(r"\n\n+", markdown.strip())
            abstract = paragraphs[0][:500] if paragraphs else ""

            # Extract title from first heading or use URL
            title_match = re.search(r"^#\s+(.+)$", markdown, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else f"Content from {source_name}"

            # Create entry
            entry = KnowledgeEntry(
                title=title,
                url=url,
                authors=source_name,
                year=date.today().year,
                abstract=abstract,
                venue=source_name,
                evidence_type="expert_opinion" if "nngroup" in url.lower() else "blog",
            )

            return entry

        except Exception as e:
            logger.warning(f"Failed to parse crawl result from {url}: {e}")
            return None


# =============================================================================
# KNOWLEDGE BASE MANAGER
# =============================================================================


class KnowledgeBaseManager:
    """Manages the SECOND-KNOWLEDGE-BRAIN.md knowledge base."""

    def __init__(self, brain_path: Path = BRAIN_PATH):
        """Initialize with path to knowledge base.

        Args:
            brain_path: Path to SECOND-KNOWLEDGE-BRAIN.md file.
        """
        self.brain_path = brain_path
        self.seen_hashes: Set[str] = load_seen_hashes()

    def append_entries(
        self, entries: List[KnowledgeEntry], dry_run: bool = False
    ) -> CrawlerStats:
        """Append new knowledge entries to the knowledge base.

        Args:
            entries: List of KnowledgeEntry objects to append.
            dry_run: If True, simulate without writing.

        Returns:
            CrawlerStats with execution metrics.
        """
        stats = CrawlerStats()
        stats.total_fetched = len(entries)

        # Score and filter entries
        scored_entries = []
        for entry in entries:
            scored_entry = dataclasses.replace(
                entry,
                relevance_score=compute_relevance_score(entry),
                evidence_type=entry.evidence_type or infer_evidence_type(entry),
            )
            scored_entries.append(scored_entry)

        # Sort by relevance score
        scored_entries.sort(key=lambda e: e.relevance_score, reverse=True)

        # Filter duplicates and low-quality entries
        new_blocks = []
        for entry in scored_entries:
            # Skip entries with very low relevance
            if entry.relevance_score < 0.15:
                continue

            url_hash = compute_url_hash(entry.url)
            if url_hash in self.seen_hashes:
                stats.duplicates_skipped += 1
                continue

            self.seen_hashes.add(url_hash)
            new_blocks.append(format_entry_block(entry))

        if not new_blocks:
            logger.info("No new entries to append")
            return stats

        # Prepare append content
        today = date.today().isoformat()
        append_content = f"\n\n## Automated Crawl Batch — {today}\n\n"
        append_content += "\n\n".join(new_blocks) + "\n"

        if dry_run:
            logger.info(f"[DRY RUN] Would append {len(new_blocks)} entries")
            stats.unique_entries = len(new_blocks)
            return stats

        # Write to knowledge base
        try:
            with open(self.brain_path, "a", encoding="utf-8") as f:
                f.write(append_content)
            stats.unique_entries = len(new_blocks)
            logger.info(f"Successfully appended {len(new_blocks)} new entries to knowledge base")
        except Exception as e:
            logger.error(f"Failed to write to knowledge base: {e}")

        return stats

    def update_log(self, stats: CrawlerStats) -> None:
        """Append execution summary to the knowledge update log section.

        Args:
            stats: CrawlerStats from execution.
        """
        log_entry = f"""
- [{date.today().isoformat()}] Crawler execution completed:
  - Total fetched: {stats.total_fetched}
  - Unique added: {stats.unique_entries}
  - Duplicates skipped: {stats.duplicates_skipped}
  - Execution time: {stats.execution_time_seconds:.2f}s
"""

        try:
            content = self.brain_path.read_text(encoding="utf-8")

            # Find or create Knowledge Update Log section
            if "## 7. Knowledge Update Log" in content:
                # Append to existing log section
                updated_content = content.replace(
                    "## 7. Knowledge Update Log",
                    f"## 7. Knowledge Update Log{log_entry}"
                )
                self.brain_path.write_text(updated_content, encoding="utf-8")
            else:
                # Add log section at end
                with open(self.brain_path, "a", encoding="utf-8") as f:
                    f.write(f"\n\n## 7. Knowledge Update Log{log_entry}\n")

        except Exception as e:
            logger.error(f"Failed to update execution log: {e}")


# =============================================================================
# MAIN ORCHESTRATOR
# =============================================================================


def main() -> int:
    """Main entry point for knowledge updater execution.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    import time

    start_time = time.time()

    logger.info(f"Starting knowledge updater for skill #{SKILL_ID} ({SKILL_SLUG})")

    # Ensure directories exist
    LOGS_PATH.mkdir(parents=True, exist_ok=True)
    (PROJECT_ROOT / ".cache").mkdir(parents=True, exist_ok=True)

    # Initialize fetchers
    arxiv_fetcher = ArxivFetcher(categories=ARXIV_CATEGORIES, max_results=30)
    web_fetcher = WebCrawlerFetcher(source_configs=SOURCE_CONFIGS)

    # Fetch entries from all sources
    all_entries = []

    logger.info("Fetching from arXiv...")
    try:
        arxiv_entries = arxiv_fetcher.fetch()
        all_entries.extend(arxiv_entries)
        logger.info(f"Retrieved {len(arxiv_entries)} papers from arXiv")
    except Exception as e:
        logger.error(f"ArXiv fetcher failed: {e}")

    logger.info("Fetching from web sources...")
    try:
        web_entries = web_fetcher.fetch()
        all_entries.extend(web_entries)
        logger.info(f"Retrieved {len(web_entries)} entries from web sources")
    except Exception as e:
        logger.error(f"Web fetcher failed: {e}")

    if not all_entries:
        logger.warning("No entries fetched from any source")
        return 0

    # Initialize knowledge base manager
    manager = KnowledgeBaseManager()

    # Append entries
    stats = manager.append_entries(all_entries, dry_run=False)

    # Update execution log
    stats.execution_time_seconds = time.time() - start_time
    manager.update_log(stats)

    # Print summary
    logger.info(stats.to_summary())

    return 0 if stats.unique_entries > 0 or stats.duplicates_skipped > 0 else 1


if __name__ == "__main__":
    sys.exit(main())
