# Primary Status Table & Baselines (`iau-mdc-new-meteor-shower-gmn`)

- **Primary Status Table URLs**:
  - `https://www.ta3.sk/IAUC22DB/MDC2022/Roje/roje_lista.php` (`2026-10-20T01:51:08Z` and re-verified `2026-10-20T18:54:36Z`, `HTTP/1.1 200 OK`, `369,910` bytes, `sha256: 1e37425b8e2b2fcff742b741d7d4acc4b2522b3abfa8876e987357ab893c8454`)
  - `https://www.ta3.sk/IAUC22DB/MDC2022/Etc/streamfulldata2026.txt` (`2026-10-20T01:51:08Z` and re-verified `2026-10-20T18:54:36Z`, `HTTP/1.1 200 OK`, `1,555,028` bytes, `sha256: 08409111125e83ef2f033b27e215fb4383e0f15f6e6a3d202f7dda3a27f027fe`)
  - `https://www.ta3.sk/IAUC22DB/MDC2022/Dokumenty/new_reports.php` (`2026-10-20T01:51:08Z`, `HTTP/1.1 200 OK`, `9,216` bytes, `sha256: 229c16a856f5539fd7b4ba22057c11921f05dd50a64231559adb590a8444b47f`)
- **Live Table Contents (`streamfulldata2026.txt`)**:
  - Header timestamp: `Last update: Oct 19, 20:00:00 UTC, 2026 Modified by R. Rudawska, M. Hajdukova and T.J.Jopek`.
  - Contains `2,192` shower solution rows (`LP = 00001..02645` across all status codes `s in {-9..-1, 0, 1, 2}`: Established, Working List, Pending, and Permanently Removed), including `1,999` explicit heliocentric orbit rows and `193` radiant-only rows (`172` with valid $V_g$ enabling exact Keplerian orbit derivation).
  - None of our four certified Main clusters (`M2_Hercules` $\min D_{\text{SH}} = 0.3539$, $\Delta\theta = 11.76^\circ$; `M1_Cepheus_Core` $\min D_{\text{SH}} = 0.2766$, $\Delta\theta = 19.94^\circ$; `M1_Cepheus_MC` $\min D_{\text{SH}} = 0.2829$, $\Delta\theta = 19.45^\circ$; `M3_Camelopardalis` $\min D_{\text{SH}} = 0.3151$, $\Delta\theta = 9.12^\circ$) or the `p1` 2025-Sep-01 4.84h outburst ($\min D_{\text{SH}} = 0.2521$, $\Delta\theta = 20.65^\circ$) matches any entry in `streamfulldata2026.txt`.
  - All `17` certified `p2` multi-year recurrent working-list showers (`M2025-S1`, `M2025-U1`, `AAQ #927`, `KCA #793`, `FDR #1206`, etc.) are currently listed in `streamfulldata2026.txt` as single-year `status == 0` working-list detections (`activity` equal to a single 4-digit year).
