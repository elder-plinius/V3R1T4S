#[allow(unused)]
pub const N: usize = 18;
#[allow(unused)]
pub const I: usize = 5;

#[allow(unused)]
pub fn run(input: [usize; 18]) -> usize {
    select_0(input)
}

/// n = 1
fn select_1([a]: [usize; 1]) -> usize {
    a
}
/// n = 2, i = 0
fn select_2([a, b]: [usize; 2]) -> usize {
    if a < b {
        select_1([a])
    } else {
        select_1([b])
    }
}
/// n = 3, i = 0
fn select_3([a, b, c]: [usize; 3]) -> usize {
    if a < b {
        select_2([a, c])
    } else {
        select_2([b, c])
    }
}
/// n = 4, i = 0
fn select_4([a, b, c, d]: [usize; 4]) -> usize {
    if a < b {
        select_3([a, c, d])
    } else {
        select_3([b, c, d])
    }
}
/// n = 7, i = 1, a < f, a < g, b < c, b < d, b < e
fn select_5([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_3([b, f, g])
    } else {
        select_4([a, c, d, e])
    }
}
/// n = 8, i = 1, a < f, a < g, a < h, b < c, b < d, b < e
fn select_6([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_4([b, f, g, h])
    } else {
        select_4([a, c, d, e])
    }
}
/// n = 9, i = 1, a < i, b < g, b < h, c < d, c < e, c < f
fn select_7([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_5([a, c, d, e, f, b, i])
    } else {
        select_6([b, c, d, e, f, a, g, h])
    }
}
/// n = 9, i = 1, c < h, c < i, d < e, d < f, d < g
fn select_8([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_7([a, c, d, e, f, g, h, i, b])
    } else {
        select_7([b, c, d, e, f, g, h, i, a])
    }
}
/// n = 8, i = 1, a < h, b < g, c < d, c < e, c < f
fn select_9([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_5([a, c, d, e, f, b, h])
    } else {
        select_5([b, c, d, e, f, a, g])
    }
}
/// n = 3, i = 1, b < c
fn select_10([a, b, c]: [usize; 3]) -> usize {
    if a < b {
        select_1([b])
    } else {
        select_2([a, c])
    }
}
/// n = 4, i = 1, b < c, b < d
fn select_11([a, b, c, d]: [usize; 4]) -> usize {
    if c < a {
        select_2([c, d])
    } else {
        select_10([a, b, d])
    }
}
/// n = 8, i = 2, a < c, a < h, b < d, b < h, d < e, d < f, d < g
fn select_12([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_4([a, e, f, g])
    } else {
        select_11([c, b, d, h])
    }
}
/// n = 9, i = 2, a < i, b < h, c < d, c < h, c < i, d < e, d < f, d < g
fn select_13([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_12([a, c, b, d, e, f, g, i])
    } else {
        select_12([b, c, a, d, e, f, g, h])
    }
}
/// n = 9, i = 2, b < i, c < d, c < e, c < i, e < f, e < g, e < h
fn select_14([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_9([b, d, e, f, g, h, a, i])
    } else {
        select_13([a, b, c, e, f, g, h, i, d])
    }
}
/// n = 10, i = 2, c < d, c < e, c < f, e < j, f < g, f < h, f < i
fn select_15([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_8([b, d, e, f, g, h, i, a, j])
    } else {
        select_14([b, a, c, d, f, g, h, i, e])
    }
}
/// n = 12, i = 2, c < d, c < e, c < f, c < g, e < l, f < j, f < k, g < h, g < i
fn select_16([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < g {
        select_15([a, b, c, d, e, f, g, j, k, l])
    } else {
        select_15([a, b, c, d, e, g, f, h, i, l])
    }
}
/// n = 13, i = 2, c < f, c < h, d < e, d < g, d < i, g < l, h < m, i < j, i < k
fn select_17([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if c < d {
        select_15([a, b, c, f, h, d, e, g, i, m])
    } else {
        select_16([a, b, d, e, g, c, i, j, k, f, h, l])
    }
}
/// n = 5, i = 1, b < c, b < d, b < e
fn select_18([a, b, c, d, e]: [usize; 5]) -> usize {
    if c < a {
        select_3([c, d, e])
    } else {
        select_11([a, b, d, e])
    }
}
/// n = 5, i = 2, a < d, a < e, b < c, b < e
fn select_19([a, b, c, d, e]: [usize; 5]) -> usize {
    if c < d {
        select_10([c, a, e])
    } else {
        select_10([d, b, e])
    }
}
/// n = 7, i = 2, a < d, b < c, b < e, e < f, e < g
fn select_20([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_18([c, e, a, f, g])
    } else {
        select_19([a, b, c, d, e])
    }
}
/// n = 7, i = 2, c < d, c < e, e < f, e < g
fn select_21([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_20([a, c, d, b, e, f, g])
    } else {
        select_20([b, c, d, a, e, f, g])
    }
}
/// n = 5, i = 0
fn select_22([a, b, c, d, e]: [usize; 5]) -> usize {
    if a < b {
        select_4([a, c, d, e])
    } else {
        select_4([b, c, d, e])
    }
}
/// n = 7, i = 1, a < g, b < c, b < d, b < e, b < f
fn select_23([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_2([b, g])
    } else {
        select_22([a, c, d, e, f])
    }
}
/// n = 6, i = 1, a < f, b < c, b < d, b < e
fn select_24([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_2([b, f])
    } else {
        select_4([a, c, d, e])
    }
}
/// n = 8, i = 2, a < c, a < f, a < g, a < h, b < d, b < f, b < g, b < h, d < e
fn select_25([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_18([c, b, f, g, h])
    } else {
        select_24([d, a, f, g, h, e])
    }
}
/// n = 11, i = 2, a < c, a < j, a < k, b < d, b < e, b < j, b < k, d < i, e < f, e < g, e < h
fn select_26([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_23([d, e, a, f, g, h, i])
    } else {
        select_25([a, b, c, d, i, e, j, k])
    }
}
/// n = 5, i = 1, a < e, b < c, b < d
fn select_27([a, b, c, d, e]: [usize; 5]) -> usize {
    if a < b {
        select_2([b, e])
    } else {
        select_3([a, c, d])
    }
}
/// n = 8, i = 2, a < f, a < g, a < h, b < d, b < e, b < h, c < d, c < e, c < f, c < g
fn select_28([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_27([b, c, f, g, h])
    } else {
        select_27([a, c, d, e, h])
    }
}
/// n = 8, i = 2, a < g, a < h, b < d, b < e, b < f, c < e, c < f, c < g, c < h
fn select_29([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_27([d, c, e, f, a])
    } else {
        select_28([a, b, c, e, f, g, h, d])
    }
}
/// n = 10, i = 2, a < c, a < i, a < j, b < d, b < i, b < j, d < e, d < f, d < g, d < h
fn select_30([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_22([a, e, f, g, h])
    } else {
        select_18([c, b, d, i, j])
    }
}
/// n = 11, i = 2, a < k, b < d, b < i, b < j, c < e, c < i, c < j, c < k, e < f, e < g, e < h
fn select_31([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < e {
        select_29([a, b, c, d, i, j, e, k])
    } else {
        select_30([b, c, d, e, a, f, g, h, i, j])
    }
}
/// n = 11, i = 2, b < e, b < j, b < k, c < d, c < f, c < j, c < k, f < g, f < h, f < i
fn select_32([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_26([b, c, e, d, f, g, h, i, a, j, k])
    } else {
        select_31([a, b, c, e, f, g, h, i, j, k, d])
    }
}
/// n = 8, i = 2, a < d, b < c, b < e, e < f, e < g, e < h
fn select_33([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < a {
        select_24([c, e, f, g, h, a])
    } else {
        select_12([a, b, d, e, f, g, h, c])
    }
}
/// n = 8, i = 2, c < d, c < e, e < f, e < g, e < h
fn select_34([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_33([a, c, d, b, e, f, g, h])
    } else {
        select_33([b, c, d, a, e, f, g, h])
    }
}
/// n = 10, i = 3, a < j, b < e, b < f, b < j, c < d, c < f, c < j, f < g, f < h, f < i
fn select_35([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_13([a, d, b, f, g, h, i, e, j])
    } else {
        select_13([a, e, c, f, g, h, i, d, j])
    }
}
/// n = 10, i = 3, a < j, b < e, b < h, b < i, b < j, c < d, c < f, c < j, f < g, f < h, f < i
fn select_36([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < b {
        select_34([a, d, f, g, b, e, h, i])
    } else {
        select_35([a, b, c, d, e, f, g, h, i, j])
    }
}
/// n = 12, i = 3, b < e, b < h, b < k, b < l, c < d, c < f, c < h, f < g, f < k, f < l, h < i, h < j
fn select_37([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < a {
        select_32([d, f, b, e, g, h, a, i, j, k, l])
    } else {
        select_36([a, b, c, d, e, f, g, k, l, h])
    }
}
/// n = 6, i = 2, a < d, a < e, a < f, b < c, b < e, b < f
fn select_38([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if c < d {
        select_11([c, a, e, f])
    } else {
        select_11([d, b, e, f])
    }
}
/// n = 7, i = 2, a < d, a < g, b < c, b < e, b < g, e < f
fn select_39([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_11([c, e, a, f])
    } else {
        select_38([a, b, c, d, e, g])
    }
}
/// n = 8, i = 2, a < d, a < h, b < c, b < e, b < h, e < f, e < g
fn select_40([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_18([c, e, a, f, g])
    } else {
        select_38([a, b, c, d, e, h])
    }
}
/// n = 10, i = 2, a < d, a < e, a < j, b < c, b < f, b < j, e < i, f < g, f < h
fn select_41([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_39([b, a, d, c, e, i, j])
    } else {
        select_40([a, b, c, d, f, g, h, j])
    }
}
/// n = 5, i = 1, b < e, c < d
fn select_42([a, b, c, d, e]: [usize; 5]) -> usize {
    if b < c {
        select_11([a, b, c, e])
    } else {
        select_11([a, c, b, d])
    }
}
/// n = 2, i = 1
fn select_43([a, b]: [usize; 2]) -> usize {
    if a < b {
        select_1([b])
    } else {
        select_1([a])
    }
}
/// n = 4, i = 2, b < d, c < d
fn select_44([a, b, c, d]: [usize; 4]) -> usize {
    if b < a {
        select_10([a, c, d])
    } else {
        select_43([b, c])
    }
}
/// n = 6, i = 3, a < e, a < f, b < e, b < f, c < d, c < f
fn select_45([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < e {
        select_44([d, a, b, f])
    } else {
        select_10([e, c, f])
    }
}
/// n = 8, i = 3, a < d, a < h, b < e, b < f, b < h, c < e, c < f, c < h, f < g
fn select_46([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < d {
        select_42([e, a, f, g, h])
    } else {
        select_45([b, c, a, d, e, h])
    }
}
/// n = 10, i = 3, a < e, a < f, b < d, b < g, c < e, c < f, c < g, f < j, g < h, g < i
fn select_47([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_18([d, g, a, h, i])
    } else {
        select_46([b, a, c, d, e, f, j, g])
    }
}
/// n = 11, i = 3, a < g, b < d, b < h, b < k, c < e, c < g, c < h, e < f, e < k, h < i, h < j
fn select_48([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_41([e, b, d, f, a, h, i, j, g, k])
    } else {
        select_47([a, b, c, d, g, e, h, i, j, f])
    }
}
/// n = 6, i = 1, b < c, b < d, b < e, b < f
fn select_49([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if c < a {
        select_4([c, d, e, f])
    } else {
        select_18([a, b, d, e, f])
    }
}
/// n = 9, i = 2, a < d, a < i, b < c, b < e, b < i, e < f, e < g, e < h
fn select_50([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_49([c, e, a, f, g, h])
    } else {
        select_38([a, b, c, d, e, i])
    }
}
/// n = 8, i = 3, a < d, a < g, b < c, b < g, b < h, c < f, d < e, d < h
fn select_51([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_19([a, c, f, g, d])
    } else {
        select_38([b, d, e, g, c, h])
    }
}
/// n = 5, i = 2, b < d, b < e, c < d, c < e
fn select_52([a, b, c, d, e]: [usize; 5]) -> usize {
    if a < b {
        select_43([b, c])
    } else {
        select_11([a, c, d, e])
    }
}
/// n = 8, i = 3, a < e, a < h, b < c, b < d, b < g, d < h, e < f, e < g
fn select_53([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_52([c, a, d, e, h])
    } else {
        select_38([b, e, f, c, d, g])
    }
}
/// n = 9, i = 3, a < g, a < i, b < d, b < h, c < e, c < g, e < f, e < h, e < i
fn select_54([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_51([c, a, b, e, f, d, g, i])
    } else {
        select_53([c, b, d, a, e, f, h, g])
    }
}
/// n = 11, i = 3, a < g, b < d, b < k, c < e, c < g, e < f, e < h, e < k, h < i, h < j
fn select_55([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < a {
        select_50([b, e, f, d, h, a, i, j, k])
    } else {
        select_54([a, b, c, d, e, f, g, k, h])
    }
}
/// n = 12, i = 4, a < d, a < f, b < c, b < e, b < i, e < h, e < l, f < g, f < i, f < l, i < j, i < k
fn select_56([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < c {
        select_48([d, f, b, g, e, h, c, i, j, k, l])
    } else {
        select_55([c, e, a, h, f, g, d, i, j, k, l])
    }
}
/// n = 14, i = 4, a < d, a < e, a < k, a < n, b < c, b < f, e < h, f < g, f < i, f < k, i < j, i < n, k < l, k < m
fn select_57([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < e {
        select_37([c, a, f, g, d, i, j, k, l, m, e, n])
    } else {
        select_56([b, a, d, c, e, f, g, h, k, l, m, i])
    }
}
/// n = 15, i = 4, a < d, a < e, a < l, b < c, b < f, e < h, f < g, f < i, f < l, i < j, i < k, k < m, l < n, l < o
fn select_58([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if k < a {
        select_21([c, g, i, j, k, a, m])
    } else {
        select_57([a, b, c, d, e, f, g, h, i, j, l, n, o, k])
    }
}
/// n = 16, i = 4, a < d, a < e, b < c, b < f, e < h, f < g, f < i, f < j, i < l, i < n, j < k, j < m, m < o, n < p
fn select_59([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if i < a {
        select_17([c, g, j, i, l, k, n, m, a, d, e, p, o])
    } else {
        select_58([a, b, c, d, e, f, g, h, j, k, m, i, o, l, n])
    }
}
/// n = 16, i = 4, a < d, a < e, b < c, b < f, e < h, f < g, f < i, f < j, f < k, i < n, j < m, k < l, k < o, o < p
fn select_60([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if i < j {
        select_59([a, b, c, d, e, f, g, h, i, k, l, n, o, j, p, m])
    } else {
        select_59([a, b, c, d, e, f, g, h, j, k, l, m, o, i, p, n])
    }
}
/// n = 16, i = 4, a < f, b < e, c < d, c < g, g < h, g < i, g < j, g < k, i < n, j < m, k < l, k < o, o < p
fn select_61([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_60([a, c, d, f, b, g, h, e, i, j, k, l, m, n, o, p])
    } else {
        select_60([b, c, d, e, a, g, h, f, i, j, k, l, m, n, o, p])
    }
}
/// n = 6, i = 2, a < d, b < c, b < e, e < f
fn select_62([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if e < a {
        select_11([c, e, a, f])
    } else {
        select_19([a, b, c, d, e])
    }
}
/// n = 7, i = 2, a < f, b < e, b < g, c < d, c < g
fn select_63([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_62([c, a, f, d, b, e])
    } else {
        select_39([c, b, e, d, a, f, g])
    }
}
/// n = 4, i = 2, a < d, b < c
fn select_64([a, b, c, d]: [usize; 4]) -> usize {
    if c < d {
        select_43([a, c])
    } else {
        select_43([b, d])
    }
}
/// n = 6, i = 3, a < e, a < f, b < d, b < f, c < d, c < e
fn select_65([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < e {
        select_64([a, c, d, f])
    } else {
        select_64([b, c, e, f])
    }
}
/// n = 6, i = 3, a < f, b < e, b < f, c < d, c < e
fn select_66([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < d {
        select_65([a, b, c, e, d, f])
    } else {
        select_64([b, d, a, e])
    }
}
/// n = 8, i = 3, a < d, a < f, b < e, b < g, c < e, c < f, c < g, g < h
fn select_67([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < g {
        select_66([b, c, a, d, f, e])
    } else {
        select_62([a, b, e, f, g, h])
    }
}
/// n = 9, i = 3, a < g, a < h, b < d, b < h, b < i, c < e, c < g, e < f, e < i
fn select_68([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_39([b, e, f, d, a, g, i])
    } else {
        select_67([b, c, a, d, g, h, e, f])
    }
}
/// n = 9, i = 3, a < h, b < e, b < h, b < i, c < d, c < f, f < g, f < i
fn select_69([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_63([d, b, f, g, e, a, i])
    } else {
        select_68([a, b, c, e, f, g, d, h, i])
    }
}
/// n = 3, i = 2
fn select_70([a, b, c]: [usize; 3]) -> usize {
    if a < b {
        select_43([b, c])
    } else {
        select_43([a, c])
    }
}
/// n = 5, i = 3, a < e, b < e, c < d
fn select_71([a, b, c, d, e]: [usize; 5]) -> usize {
    if d < e {
        select_70([a, b, d])
    } else {
        select_43([c, e])
    }
}
/// n = 4, i = 1, a < d, b < c
fn select_72([a, b, c, d]: [usize; 4]) -> usize {
    if a < b {
        select_2([b, d])
    } else {
        select_2([a, c])
    }
}
/// n = 4, i = 1, c < d
fn select_73([a, b, c, d]: [usize; 4]) -> usize {
    if a < b {
        select_72([a, c, d, b])
    } else {
        select_72([b, c, d, a])
    }
}
/// n = 7, i = 3, a < d, b < e, b < f, c < e, c < f, f < g
fn select_74([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < f {
        select_71([b, c, a, d, e])
    } else {
        select_73([a, e, f, g])
    }
}
/// n = 8, i = 3, a < g, b < d, b < h, c < e, c < g, e < f, e < h
fn select_75([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_39([b, e, f, d, a, g, h])
    } else {
        select_74([b, a, c, d, g, e, f])
    }
}
/// n = 10, i = 4, a < e, a < i, a < j, b < d, b < g, c < f, c < g, f < i, g < h, g < j
fn select_76([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < f {
        select_75([d, a, c, e, g, h, f, j])
    } else {
        select_68([f, a, b, e, g, h, d, i, j])
    }
}
/// n = 10, i = 4, a < e, a < j, b < d, b < i, b < j, c < f, c < g, f < i, g < h, g < j
fn select_77([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_69([f, b, g, h, d, a, e, i, j])
    } else {
        select_76([b, a, c, e, d, f, g, h, i, j])
    }
}
/// n = 6, i = 2, a < e, a < f, b < d, b < f, c < d, c < e
fn select_78([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_72([b, c, e, f])
    } else {
        select_72([a, c, d, f])
    }
}
/// n = 6, i = 2, a < f, b < e, b < f, c < d, c < e
fn select_79([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < a {
        select_72([b, d, a, e])
    } else {
        select_78([a, b, c, e, d, f])
    }
}
/// n = 6, i = 2, a < f, b < e, c < d, c < e, c < f
fn select_80([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_19([a, c, d, b, f])
    } else {
        select_19([b, c, d, a, e])
    }
}
/// n = 7, i = 2, a < g, b < e, b < f, c < d, c < f, c < g
fn select_81([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < d {
        select_79([a, c, b, e, f, g])
    } else {
        select_80([a, b, c, d, f, g])
    }
}
/// n = 8, i = 2, b < e, b < h, c < d, c < f, c < h, f < g
fn select_82([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < f {
        select_81([a, b, c, d, e, h, f])
    } else {
        select_40([b, c, d, e, f, a, g, h])
    }
}
/// n = 3, i = 1
fn select_83([a, b, c]: [usize; 3]) -> usize {
    if a < b {
        select_10([c, a, b])
    } else {
        select_10([c, b, a])
    }
}
/// n = 5, i = 2, a < c, b < d, d < e
fn select_84([a, b, c, d, e]: [usize; 5]) -> usize {
    if d < a {
        select_2([a, e])
    } else {
        select_10([c, b, d])
    }
}
/// n = 6, i = 2, a < e, b < c, b < d, e < f
fn select_85([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if c < e {
        select_83([a, c, d])
    } else {
        select_84([b, a, d, e, f])
    }
}
/// n = 8, i = 2, a < d, a < g, a < h, b < c, b < g, b < h, c < e, d < f
fn select_86([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_27([c, a, g, h, e])
    } else {
        select_27([d, b, g, h, f])
    }
}
/// n = 8, i = 2, a < d, b < g, b < h, c < e, c < g, c < h, e < f
fn select_87([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_85([c, a, b, d, e, f])
    } else {
        select_86([b, c, e, a, f, d, g, h])
    }
}
/// n = 8, i = 2, c < g, c < h, d < e, d < g, d < h, e < f
fn select_88([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_87([a, c, d, b, e, f, g, h])
    } else {
        select_87([b, c, d, a, e, f, g, h])
    }
}
/// n = 10, i = 3, b < f, b < h, c < e, c < g, d < f, d < g, d < h, g < i, h < j
fn select_89([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < c {
        select_82([a, c, d, f, e, h, j, g])
    } else {
        select_88([a, e, b, d, g, i, f, h])
    }
}
/// n = 6, i = 2, a < c, a < f, b < d, b < f, d < e
fn select_90([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if c < d {
        select_10([c, b, f])
    } else {
        select_72([a, d, e, f])
    }
}
/// n = 7, i = 2, a < g, b < f, c < d, c < f, c < g, d < e
fn select_91([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_90([a, c, b, d, e, g])
    } else {
        select_90([b, c, a, d, e, f])
    }
}
/// n = 5, i = 2, a < e, b < d, c < d, c < e
fn select_92([a, b, c, d, e]: [usize; 5]) -> usize {
    if a < b {
        select_10([b, c, e])
    } else {
        select_10([a, c, d])
    }
}
/// n = 7, i = 3, a < f, a < g, b < d, b < g, c < e, c < g, e < f
fn select_93([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < e {
        select_92([a, d, c, e, g])
    } else {
        select_78([a, b, e, d, f, g])
    }
}
/// n = 9, i = 3, a < d, a < i, b < f, b < h, b < i, c < e, c < f, c < i, e < h, f < g
fn select_94([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < d {
        select_91([a, e, b, f, g, h, i])
    } else {
        select_93([b, a, c, d, e, h, i])
    }
}
/// n = 7, i = 3, a < e, a < g, b < e, b < f, c < d, d < f, d < g
fn select_95([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_72([a, b, f, g])
    } else {
        select_84([b, c, e, d, g])
    }
}
/// n = 6, i = 3, a < e, b < e, b < f, c < d, d < f
fn select_96([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < d {
        select_64([b, c, d, e])
    } else {
        select_10([a, b, f])
    }
}
/// n = 8, i = 4, a < d, a < h, b < f, c < e, c < h, e < g, f < g, f < h
fn select_97([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < d {
        select_95([a, e, b, f, d, g, h])
    } else {
        select_96([d, c, b, f, e, h])
    }
}
/// n = 10, i = 4, a < d, a < j, b < f, c < e, c < g, c < j, e < i, f < g, f < i, f < j, g < h
fn select_98([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < d {
        select_91([a, e, f, g, h, i, j])
    } else {
        select_97([a, b, c, d, e, f, i, j])
    }
}
/// n = 10, i = 4, a < e, a < j, b < d, b < h, b < j, c < f, f < g, f < h, f < j, h < i
fn select_99([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < d {
        select_94([a, b, f, e, g, h, i, d, j])
    } else {
        select_98([a, c, b, e, d, f, h, i, g, j])
    }
}
/// n = 12, i = 4, a < f, a < i, b < e, b < j, b < l, c < d, c < g, c < l, f < h, f < l, g < i, g < j, j < k
fn select_100([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < f {
        select_89([d, a, b, g, e, i, j, f, k, h])
    } else {
        select_99([b, c, a, d, e, f, h, g, i, l])
    }
}
/// n = 12, i = 4, a < f, a < j, a < l, b < e, b < h, c < d, c < g, c < l, g < j, h < i, h < l, j < k
fn select_101([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < g {
        select_77([a, c, b, d, f, e, h, i, g, l])
    } else {
        select_100([b, a, c, d, f, h, g, i, e, j, k, l])
    }
}
/// n = 5, i = 2, b < e, c < d, c < e
fn select_102([a, b, c, d, e]: [usize; 5]) -> usize {
    if a < b {
        select_64([a, c, d, b])
    } else {
        select_19([b, c, d, a, e])
    }
}
/// n = 6, i = 2, b < e, b < f, c < d, c < f
fn select_103([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < e {
        select_102([a, b, c, d, f])
    } else {
        select_102([a, c, b, e, f])
    }
}
/// n = 5, i = 2, a < e, b < e, c < d
fn select_104([a, b, c, d, e]: [usize; 5]) -> usize {
    if a < b {
        select_84([c, a, d, b, e])
    } else {
        select_84([c, b, d, a, e])
    }
}
/// n = 6, i = 3, a < f, b < e, c < d, c < f
fn select_105([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if e < d {
        select_96([a, c, b, e, f, d])
    } else {
        select_104([b, d, a, f, e])
    }
}
/// n = 7, i = 3, b < e, b < g, c < d, c < f, f < g
fn select_106([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < a {
        select_103([d, b, f, a, e, g])
    } else {
        select_105([a, b, c, d, e, f])
    }
}
/// n = 5, i = 2, a < e, b < c, b < d
fn select_107([a, b, c, d, e]: [usize; 5]) -> usize {
    if c < d {
        select_84([a, b, e, c, d])
    } else {
        select_84([a, b, e, d, c])
    }
}
/// n = 7, i = 3, a < d, a < e, b < e, b < f, c < d, c < f, f < g
fn select_108([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < d {
        select_84([a, c, e, f, g])
    } else {
        select_64([b, c, d, e])
    }
}
/// n = 7, i = 3, a < g, b < f, b < g, c < d, c < f, d < e
fn select_109([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_107([b, d, a, e, f])
    } else {
        select_108([b, a, c, f, g, d, e])
    }
}
/// n = 8, i = 3, b < e, b < g, c < d, c < g, c < h, d < f, e < h
fn select_110([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_109([a, b, c, d, f, g, e])
    } else {
        select_51([b, c, d, e, a, f, g, h])
    }
}
/// n = 8, i = 3, b < e, c < g, c < h, d < f, d < g, f < h
fn select_111([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < c {
        select_106([a, d, b, e, f, c, g])
    } else {
        select_110([a, d, c, b, f, e, g, h])
    }
}
/// n = 8, i = 4, a < f, a < g, b < e, b < h, c < d, c < f, e < g, f < h
fn select_112([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < d {
        select_108([e, a, c, d, g, f, h])
    } else {
        select_96([d, b, a, f, e, h])
    }
}
/// n = 9, i = 4, a < d, b < f, b < h, c < e, c < g, e < h, e < i, f < g, f < i
fn select_113([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < e {
        select_112([c, b, a, d, f, e, g, h])
    } else {
        select_51([b, e, a, f, g, d, h, i])
    }
}
/// n = 7, i = 3, a < d, b < f, b < g, c < e, c < f, e < g
fn select_114([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < e {
        select_66([b, c, a, d, e, f])
    } else {
        select_90([b, e, f, a, d, g])
    }
}
/// n = 7, i = 3, a < g, b < f, c < e, d < f, d < g
fn select_115([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_114([c, d, a, e, b, g, f])
    } else {
        select_114([c, d, b, e, a, f, g])
    }
}
/// n = 9, i = 4, a < e, b < f, b < h, c < d, c < g, f < i, g < h, g < i
fn select_116([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < d {
        select_113([a, b, c, e, g, f, d, h, i])
    } else {
        select_115([d, g, a, b, e, h, f])
    }
}
/// n = 9, i = 4, a < f, b < e, b < i, c < d, c < g, g < h, g < i
fn select_117([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if h < e {
        select_111([d, a, b, g, f, h, i, e])
    } else {
        select_116([a, b, c, d, f, e, g, i, h])
    }
}
/// n = 9, i = 2, a < c, a < d, b < e, e < f, e < g, e < h, e < i
fn select_118([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_22([a, f, g, h, i])
    } else {
        select_73([c, d, b, e])
    }
}
/// n = 11, i = 3, a < d, a < e, b < d, b < f, c < e, c < f, e < k, f < g, f < h, f < i, f < j
fn select_119([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_22([a, g, h, i, j])
    } else {
        select_90([b, c, d, e, k, f])
    }
}
/// n = 11, i = 3, a < f, b < f, b < g, c < d, c < g, d < e, g < h, g < i, g < j, g < k
fn select_120([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_118([d, b, a, e, g, h, i, j, k])
    } else {
        select_119([a, b, c, f, d, g, h, i, j, k, e])
    }
}
/// n = 11, i = 3, a < d, a < e, b < f, b < k, c < e, c < f, d < k, f < g, f < h, f < i, f < j
fn select_121([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_22([a, g, h, i, j])
    } else {
        select_79([d, b, c, e, f, k])
    }
}
/// n = 11, i = 3, a < f, b < e, c < f, c < g, d < e, d < g, g < h, g < i, g < j, g < k
fn select_122([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_121([a, d, c, b, f, g, h, i, j, k, e])
    } else {
        select_121([b, c, d, a, e, g, h, i, j, k, f])
    }
}
/// n = 11, i = 3, b < f, c < f, c < g, d < e, d < g, g < h, g < i, g < j, g < k
fn select_123([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_120([b, c, d, e, a, f, g, h, i, j, k])
    } else {
        select_122([a, b, d, c, f, e, g, h, i, j, k])
    }
}
/// n = 9, i = 4, a < d, a < i, b < f, b < h, c < e, c < g, c < i, e < h, f < g, f < i
fn select_124([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < e {
        select_46([a, c, f, d, g, e, h, i])
    } else {
        select_74([a, b, e, d, h, f, g])
    }
}
/// n = 9, i = 4, a < e, a < i, b < g, b < h, c < d, c < f, c < i, f < h, g < i
fn select_125([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < d {
        select_124([a, b, c, e, f, g, d, h, i])
    } else {
        select_115([d, f, a, b, e, h, g])
    }
}
/// n = 12, i = 4, a < f, a < i, b < e, b < h, b < i, c < d, c < g, c < i, g < h, i < j, i < k, i < l
fn select_126([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if i < e {
        select_123([d, g, b, a, f, h, i, e, j, k, l])
    } else {
        select_125([a, b, c, d, f, g, e, h, i])
    }
}
/// n = 13, i = 4, a < f, a < j, b < e, b < i, b < j, c < d, c < g, c < j, g < h, g < i, j < k, j < l, j < m
fn select_127([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if h < j {
        select_117([a, b, c, d, e, f, g, h, i])
    } else {
        select_126([a, b, c, d, e, f, g, i, j, k, l, m])
    }
}
/// n = 8, i = 2, a < c, b < d, d < e, d < f, d < g, d < h
fn select_128([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_22([a, e, f, g, h])
    } else {
        select_10([c, b, d])
    }
}
/// n = 10, i = 3, a < d, a < e, b < e, b < f, c < d, c < f, f < g, f < h, f < i, f < j
fn select_129([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_22([a, g, h, i, j])
    } else {
        select_19([b, c, d, e, f])
    }
}
/// n = 10, i = 3, a < e, b < e, b < f, c < d, c < f, f < g, f < h, f < i, f < j
fn select_130([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_128([d, b, a, f, g, h, i, j])
    } else {
        select_129([a, b, c, d, e, f, g, h, i, j])
    }
}
/// n = 6, i = 2, a < f, b < f, c < d, d < e
fn select_131([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < a {
        select_11([b, d, a, e])
    } else {
        select_92([b, c, a, d, f])
    }
}
/// n = 8, i = 3, a < e, a < h, b < e, b < g, c < d, d < g, d < h, e < f
fn select_132([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < d {
        select_10([c, e, f])
    } else {
        select_92([a, b, d, g, h])
    }
}
/// n = 8, i = 3, a < e, b < f, b < h, c < d, c < f, e < h, f < g
fn select_133([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_131([a, d, b, f, g, e])
    } else {
        select_132([b, c, a, e, f, g, d, h])
    }
}
/// n = 8, i = 2, a < c, a < h, b < d, b < h, c < g, d < e, d < f
fn select_134([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_3([a, e, f])
    } else {
        select_27([c, b, d, h, g])
    }
}
/// n = 9, i = 3, a < e, a < h, a < i, b < e, b < g, b < i, c < d, c < i, d < g, d < h, e < f
fn select_135([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < d {
        select_72([c, e, f, i])
    } else {
        select_78([a, b, d, g, h, i])
    }
}
/// n = 10, i = 3, a < f, a < i, a < j, b < e, b < f, b < j, c < d, c < e, c < j, d < i, e < g, f < h
fn select_136([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < d {
        select_134([a, c, f, e, d, g, h, j])
    } else {
        select_135([a, b, c, d, f, h, e, i, j])
    }
}
/// n = 7, i = 2, a < d, a < g, b < c, b < g, c < e, d < f
fn select_137([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < d {
        select_72([a, c, e, g])
    } else {
        select_72([b, d, f, g])
    }
}
/// n = 11, i = 4, a < f, a < g, a < j, a < k, b < d, b < j, c < e, c < k, d < f, d < i, d < k, e < g, e < i, e < j, g < h
fn select_138([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_90([a, c, f, e, i, k])
    } else {
        select_137([a, b, d, g, i, h, j])
    }
}
/// n = 12, i = 4, a < f, a < h, a < k, a < l, b < d, b < g, b < k, c < e, c < l, d < f, d < l, e < g, e < h, e < k, g < i, h < j
fn select_139([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < d {
        select_134([a, b, h, g, d, i, j, k])
    } else {
        select_138([a, b, c, d, e, f, h, j, g, k, l])
    }
}
/// n = 12, i = 4, a < f, a < g, a < i, a < l, b < d, b < h, b < l, c < e, c < f, d < g, e < h, e < i, e < l, h < j, i < k
fn select_140([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < d {
        select_136([b, e, a, f, i, h, k, j, d, l])
    } else {
        select_139([a, b, c, d, e, g, h, i, j, k, l, f])
    }
}
/// n = 12, i = 4, a < g, a < i, a < l, b < e, b < h, b < l, c < d, c < f, e < g, f < h, f < i, f < l, h < j, i < k
fn select_141([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < a {
        select_133([d, f, b, e, a, h, j, i])
    } else {
        select_140([a, b, c, e, f, d, g, h, i, j, k, l])
    }
}
/// n = 15, i = 4, a < g, a < i, a < j, b < e, b < h, b < j, c < d, c < f, c < j, e < g, f < h, f < i, h < k, i < l, j < m, j < n, j < o
fn select_142([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if j < f {
        select_130([e, a, c, d, g, j, f, m, n, o])
    } else {
        select_141([a, b, c, d, e, f, g, h, i, k, l, j])
    }
}
/// n = 15, i = 4, a < f, a < i, a < j, b < e, b < h, b < j, c < d, c < g, c < j, g < h, g < i, h < k, i < l, j < m, j < n, j < o
fn select_143([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if e < f {
        select_142([a, b, c, d, e, g, f, h, i, j, k, l, m, n, o])
    } else {
        select_142([b, a, c, d, f, g, e, i, h, j, l, k, m, n, o])
    }
}
/// n = 15, i = 4, a < f, a < j, a < k, b < e, b < g, b < k, c < d, c < h, c < k, g < i, h < j, j < l, k < m, k < n, k < o
fn select_144([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < h {
        select_127([a, c, b, e, d, f, g, i, h, k, m, n, o])
    } else {
        select_143([a, b, c, d, e, f, h, g, j, k, i, l, m, n, o])
    }
}
/// n = 15, i = 4, a < h, b < g, b < k, c < f, c < j, c < k, d < e, d < i, d < k, i < j, j < l, k < m, k < n, k < o
fn select_145([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if a < b {
        select_101([c, a, d, e, h, f, i, b, g, j, l, k])
    } else {
        select_144([c, b, d, e, g, f, a, i, h, j, k, l, m, n, o])
    }
}
/// n = 8, i = 1, b < g, b < h, c < d, c < e, c < f
fn select_146([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_24([a, c, d, e, f, b])
    } else {
        select_6([b, c, d, e, f, a, g, h])
    }
}
/// n = 9, i = 1, b < i, c < h, d < e, d < f, d < g
fn select_147([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if b < c {
        select_146([a, b, d, e, f, g, c, i])
    } else {
        select_146([a, c, d, e, f, g, b, h])
    }
}
/// n = 11, i = 1, b < k, c < j, d < h, d < i, e < f, e < g
fn select_148([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_147([a, b, c, d, e, h, i, j, k])
    } else {
        select_147([a, b, c, e, d, f, g, j, k])
    }
}
/// n = 7, i = 1, b < g, c < d, c < e, c < f
fn select_149([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_24([a, c, d, e, f, b])
    } else {
        select_5([b, c, d, e, f, a, g])
    }
}
/// n = 7, i = 2, a < c, a < f, a < g, b < d, b < f, b < g, d < e
fn select_150([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < d {
        select_11([c, b, f, g])
    } else {
        select_27([d, a, f, g, e])
    }
}
/// n = 6, i = 1, a < e, a < f, b < c, b < d
fn select_151([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_3([b, e, f])
    } else {
        select_3([a, c, d])
    }
}
/// n = 8, i = 2, a < c, a < g, a < h, b < d, b < g, b < h, d < e, d < f
fn select_152([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_11([c, b, g, h])
    } else {
        select_151([a, d, e, f, g, h])
    }
}
/// n = 8, i = 2, a < d, a < g, a < h, b < c, b < e, b < g, b < h, e < f
fn select_153([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < e {
        select_150([a, b, d, c, e, g, h])
    } else {
        select_152([a, b, d, e, c, f, g, h])
    }
}
/// n = 10, i = 2, a < d, a < j, b < c, b < e, b < f, b < j, e < i, f < g, f < h
fn select_154([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_149([c, e, f, a, g, h, i])
    } else {
        select_153([a, b, c, d, e, i, f, j])
    }
}
/// n = 8, i = 1, a < g, a < h, b < c, b < d, b < e, b < f
fn select_155([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_3([b, g, h])
    } else {
        select_22([a, c, d, e, f])
    }
}
/// n = 8, i = 1, b < h, c < d, c < e, c < f, c < g
fn select_156([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_23([a, c, d, e, f, g, b])
    } else {
        select_155([b, c, d, e, f, g, a, h])
    }
}
/// n = 11, i = 2, a < d, a < k, b < c, b < e, b < f, b < k, e < j, f < g, f < h, f < i
fn select_157([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_156([c, e, f, a, g, h, i, j])
    } else {
        select_153([a, b, c, d, e, j, f, k])
    }
}
/// n = 12, i = 2, a < d, a < l, b < c, b < e, b < f, b < g, b < l, e < k, f < j, g < h, g < i
fn select_158([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < g {
        select_154([a, b, c, d, f, e, g, k, j, l])
    } else {
        select_157([a, b, c, d, f, g, e, h, i, j, l])
    }
}
/// n = 13, i = 2, a < d, b < c, b < e, b < f, b < g, b < h, e < m, f < l, g < k, h < i, h < j
fn select_159([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if e < a {
        select_148([c, f, g, e, h, i, j, a, m, k, l])
    } else {
        select_158([a, b, c, d, f, g, h, i, j, k, l, e])
    }
}
/// n = 11, i = 2, a < c, a < k, b < d, b < e, b < k, d < j, e < f, e < g, e < h, e < i
fn select_160([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_155([d, e, f, g, h, i, a, j])
    } else {
        select_30([a, b, c, e, f, g, h, i, d, k])
    }
}
/// n = 13, i = 3, a < d, a < g, a < h, b < c, b < g, b < h, c < e, d < f, g < m, h < i, h < j, h < k, h < l
fn select_161([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if c < d {
        select_160([c, a, e, g, h, i, j, k, l, m, d])
    } else {
        select_160([d, b, f, g, h, i, j, k, l, m, c])
    }
}
/// n = 16, i = 3, a < d, a < l, b < c, b < e, b < l, c < g, d < h, e < f, e < i, e < j, e < k, i < o, j < n, k < m, l < p
fn select_162([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < a {
        select_159([c, e, f, g, i, j, k, a, d, l, m, n, o])
    } else {
        select_161([a, b, c, d, g, h, l, e, f, i, j, k, p])
    }
}
/// n = 6, i = 0
fn select_163([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_22([a, c, d, e, f])
    } else {
        select_22([b, c, d, e, f])
    }
}
/// n = 9, i = 1, a < h, a < i, b < c, b < d, b < e, b < f, b < g
fn select_164([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_3([b, h, i])
    } else {
        select_163([a, c, d, e, f, g])
    }
}
/// n = 10, i = 2, a < c, a < j, b < d, b < j, d < e, d < f, d < g, d < h, d < i
fn select_165([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_163([a, e, f, g, h, i])
    } else {
        select_11([c, b, d, j])
    }
}
/// n = 11, i = 2, a < c, b < d, b < e, d < k, e < f, e < g, e < h, e < i, e < j
fn select_166([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_164([d, e, f, g, h, i, j, a, k])
    } else {
        select_165([a, b, c, e, f, g, h, i, j, d])
    }
}
/// n = 9, i = 3, a < d, a < f, a < i, b < d, b < e, b < i, c < e, c < f, c < i, e < g, f < h
fn select_167([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < f {
        select_90([a, c, d, e, g, i])
    } else {
        select_90([b, c, d, f, h, i])
    }
}
/// n = 9, i = 3, a < f, a < i, b < f, b < g, b < i, c < d, c < g, c < i, d < e, g < h
fn select_168([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_85([b, d, a, e, g, h])
    } else {
        select_167([a, b, c, f, g, d, h, e, i])
    }
}
/// n = 13, i = 3, a < f, b < f, b < g, b < h, c < d, c < g, c < h, d < e, g < m, h < i, h < j, h < k, h < l
fn select_169([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if h < a {
        select_166([d, b, e, g, h, a, i, j, k, l, m])
    } else {
        select_168([a, b, c, d, e, f, g, m, h])
    }
}
/// n = 16, i = 3, a < h, b < d, b < l, c < e, c < h, c < l, d < g, e < f, e < i, e < j, e < k, i < o, j < n, k < m, l < p
fn select_170([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < b {
        select_159([a, e, f, h, i, j, k, b, d, l, m, n, o])
    } else {
        select_169([a, c, b, d, g, h, l, e, f, i, j, k, p])
    }
}
/// n = 16, i = 3, b < e, b < l, c < d, c < f, c < l, e < h, f < g, f < i, f < j, f < k, i < o, j < n, k < m, l < p
fn select_171([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if d < a {
        select_162([b, c, d, e, f, g, a, h, i, j, k, l, m, n, o, p])
    } else {
        select_170([a, b, c, e, f, g, h, d, i, j, k, l, m, n, o, p])
    }
}
/// n = 9, i = 2, a < c, b < d, c < i, d < e, d < f, d < g, d < h
fn select_172([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_22([a, e, f, g, h])
    } else {
        select_72([b, c, i, d])
    }
}
/// n = 5, i = 1, c < d, c < e
fn select_173([a, b, c, d, e]: [usize; 5]) -> usize {
    if a < b {
        select_27([a, c, d, e, b])
    } else {
        select_27([b, c, d, e, a])
    }
}
/// n = 10, i = 2, a < c, a < d, a < j, b < e, b < j, e < f, e < g, e < h, e < i
fn select_174([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_22([a, f, g, h, i])
    } else {
        select_173([c, d, b, e, j])
    }
}
/// n = 10, i = 2, b < d, b < j, c < e, c < j, e < f, e < g, e < h, e < i
fn select_175([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_172([a, c, b, e, f, g, h, i, d])
    } else {
        select_174([b, c, a, d, e, f, g, h, i, j])
    }
}
/// n = 6, i = 2, a < e, a < f, b < c, b < d, b < f
fn select_176([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if c < d {
        select_90([a, b, e, c, d, f])
    } else {
        select_90([a, b, e, d, c, f])
    }
}
/// n = 11, i = 3, a < d, a < e, a < f, b < f, b < g, c < d, c < e, c < g, g < h, g < i, g < j, g < k
fn select_177([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_22([a, h, i, j, k])
    } else {
        select_176([b, c, d, e, f, g])
    }
}
/// n = 11, i = 3, a < e, a < f, b < f, b < g, c < d, c < e, c < g, g < h, g < i, g < j, g < k
fn select_178([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_172([d, b, a, g, h, i, j, k, e])
    } else {
        select_177([a, b, c, d, e, f, g, h, i, j, k])
    }
}
/// n = 12, i = 3, a < f, b < f, b < g, b < l, c < d, c < e, c < g, e < l, g < h, g < i, g < j, g < k
fn select_179([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < a {
        select_175([d, e, b, a, g, h, i, j, k, l])
    } else {
        select_178([a, b, c, d, e, f, g, h, i, j, k])
    }
}
/// n = 15, i = 3, a < h, b < d, b < e, c < f, c < h, c < o, e < o, f < g, f < i, f < j, f < k, i < n, j < m, k < l
fn select_180([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if f < b {
        select_159([a, f, g, h, i, j, k, b, d, e, l, m, n])
    } else {
        select_179([a, c, b, d, e, h, f, g, i, j, k, o])
    }
}
/// n = 10, i = 2, b < i, b < j, c < d, c < i, c < j, d < e, d < f, d < g, d < h
fn select_181([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_128([a, c, b, d, e, f, g, h])
    } else {
        select_30([b, c, a, d, e, f, g, h, i, j])
    }
}
/// n = 11, i = 3, a < d, a < e, a < k, b < e, b < f, b < k, c < d, c < f, c < k, f < g, f < h, f < i, f < j
fn select_182([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_22([a, g, h, i, j])
    } else {
        select_38([b, c, d, e, f, k])
    }
}
/// n = 11, i = 3, a < e, a < k, b < e, b < f, b < k, c < d, c < f, c < k, f < g, f < h, f < i, f < j
fn select_183([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_128([d, b, a, f, g, h, i, j])
    } else {
        select_182([a, b, c, d, e, f, g, h, i, j, k])
    }
}
/// n = 13, i = 4, a < f, a < g, a < h, b < e, b < h, b < m, c < d, c < f, c < h, e < g, f < m, h < i, h < j, h < k, h < l
fn select_184([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if f < e {
        select_181([d, f, b, h, i, j, k, l, e, m])
    } else {
        select_183([e, a, c, d, g, h, i, j, k, l, f])
    }
}
/// n = 16, i = 4, a < d, a < f, b < f, b < g, b < i, c < e, c < g, c < p, e < i, f < p, g < h, g < j, g < k, g < l, j < o, k < n, l < m
fn select_185([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if g < a {
        select_159([e, g, h, i, j, k, l, a, d, f, m, n, o])
    } else {
        select_184([b, c, a, d, e, f, i, g, h, j, k, l, p])
    }
}
/// n = 16, i = 4, a < f, a < g, b < e, b < h, b < p, c < d, c < g, c < h, g < p, h < i, h < j, h < k, h < l, j < o, k < n, l < m
fn select_186([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if d < e {
        select_180([d, a, b, f, g, h, i, e, j, k, l, m, n, o, p])
    } else {
        select_185([a, c, b, f, e, g, h, i, d, j, k, l, m, n, o, p])
    }
}
/// n = 17, i = 4, a < f, b < e, b < h, b < m, c < d, c < g, c < h, g < m, h < i, h < j, h < k, h < l, j < p, k < o, l < n, m < q
fn select_187([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if g < a {
        select_171([d, g, b, e, a, h, i, f, j, k, l, m, n, o, p, q])
    } else {
        select_186([a, b, c, d, e, f, g, h, i, j, k, l, n, o, p, m])
    }
}
/// n = 17, i = 4, a < h, b < g, c < f, c < j, c < n, d < e, d < i, d < j, i < n, j < k, j < l, j < m, l < p, m < o, n < q
fn select_188([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if b < j {
        select_145([a, b, c, d, e, f, g, h, i, n, j, q, k, l, m])
    } else {
        select_187([a, c, d, e, f, h, i, j, k, b, l, m, n, o, p, g, q])
    }
}
/// n = 17, i = 4, a < h, b < g, c < f, c < i, d < e, d < j, d < p, i < p, j < k, j < l, j < m, l < o, m < n, p < q
fn select_189([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if j < c {
        select_61([a, b, d, e, g, h, j, k, l, m, c, f, n, o, i, p])
    } else {
        select_188([a, b, d, c, f, e, g, h, i, j, k, l, m, p, n, o, q])
    }
}
/// n = 10, i = 2, a < c, b < d, b < e, d < i, d < j, e < f, e < g, e < h
fn select_190([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_6([d, e, f, g, h, a, i, j])
    } else {
        select_12([a, b, c, e, f, g, h, d])
    }
}
/// n = 10, i = 2, c < d, c < e, d < i, d < j, e < f, e < g, e < h
fn select_191([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_190([a, c, b, d, e, f, g, h, i, j])
    } else {
        select_190([b, c, a, d, e, f, g, h, i, j])
    }
}
/// n = 11, i = 2, c < d, c < e, c < f, d < k, e < j, f < g, f < h, f < i
fn select_192([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_191([a, b, c, d, f, g, h, i, e, k])
    } else {
        select_191([a, b, c, e, f, g, h, i, d, j])
    }
}
/// n = 12, i = 2, c < e, c < h, c < l, d < f, d < g, d < l, f < j, g < i, h < k
fn select_193([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if c < d {
        select_15([a, b, c, e, h, d, f, g, l, k])
    } else {
        select_192([a, b, d, f, g, c, e, h, l, i, j])
    }
}
/// n = 14, i = 2, c < e, c < h, d < f, d < g, d < i, f < m, g < l, h < n, i < j, i < k
fn select_194([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < c {
        select_192([a, b, d, f, g, i, c, j, k, l, m])
    } else {
        select_193([a, b, c, d, e, f, g, h, l, m, n, i])
    }
}
/// n = 17, i = 4, a < d, a < e, b < c, b < f, e < h, f < g, f < i, f < j, i < k, i < n, j < l, j < m, l < p, m < o, n < q
fn select_195([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if j < a {
        select_194([c, g, i, j, k, l, m, n, a, d, e, o, p, q])
    } else {
        select_58([a, b, c, d, e, f, g, h, i, k, n, j, q, l, m])
    }
}
/// n = 17, i = 4, a < d, a < e, b < c, b < f, e < h, f < g, f < i, f < j, f < k, i < m, j < l, k < n, k < o, n < q, o < p
fn select_196([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if i < j {
        select_195([a, b, c, d, e, f, g, h, i, k, m, n, o, j, p, q, l])
    } else {
        select_195([a, b, c, d, e, f, g, h, j, k, l, n, o, i, p, q, m])
    }
}
/// n = 17, i = 4, a < f, b < e, c < d, c < g, g < h, g < i, g < j, g < k, i < m, j < l, k < n, k < o, n < q, o < p
fn select_197([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if a < b {
        select_196([a, c, d, f, b, g, h, e, i, j, k, l, m, n, o, p, q])
    } else {
        select_196([b, c, d, e, a, g, h, f, i, j, k, l, m, n, o, p, q])
    }
}
/// n = 10, i = 1, a < i, a < j, b < g, b < h, c < d, c < e, c < f
fn select_198([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_6([a, c, d, e, f, b, i, j])
    } else {
        select_6([b, c, d, e, f, a, g, h])
    }
}
/// n = 11, i = 1, a < k, b < j, c < h, c < i, d < e, d < f, d < g
fn select_199([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_198([a, c, d, e, f, g, h, i, b, k])
    } else {
        select_198([b, c, d, e, f, g, h, i, a, j])
    }
}
/// n = 11, i = 1, c < k, d < i, d < j, e < f, e < g, e < h
fn select_200([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_199([a, c, d, e, f, g, h, i, j, k, b])
    } else {
        select_199([b, c, d, e, f, g, h, i, j, k, a])
    }
}
/// n = 12, i = 1, c < l, d < k, e < j, f < g, f < h, f < i
fn select_201([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if c < d {
        select_200([a, b, e, c, f, g, h, i, d, l, j])
    } else {
        select_200([a, b, e, d, f, g, h, i, c, k, j])
    }
}
/// n = 8, i = 2, a < g, a < h, b < e, b < f, c < d, c < f, c < g, c < h
fn select_202([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < a {
        select_176([c, b, a, e, d, f])
    } else {
        select_150([c, a, d, b, e, g, h])
    }
}
/// n = 9, i = 2, a < i, b < e, b < h, c < d, c < f, c < h, c < i, f < g
fn select_203([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_40([b, c, d, e, f, a, g, h])
    } else {
        select_202([a, b, c, d, e, h, f, i])
    }
}
/// n = 11, i = 2, b < e, b < k, c < d, c < f, c < g, c < k, f < j, g < h, g < i
fn select_204([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < g {
        select_203([a, b, c, d, e, f, j, k, g])
    } else {
        select_157([b, c, d, e, f, g, a, h, i, j, k])
    }
}
/// n = 12, i = 2, b < e, b < l, c < d, c < f, c < g, c < h, c < l, f < k, g < j, h < i
fn select_205([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < g {
        select_204([a, b, c, d, e, h, f, g, k, i, l])
    } else {
        select_204([a, b, c, d, e, h, g, f, j, i, l])
    }
}
/// n = 14, i = 2, b < e, c < d, c < f, c < g, c < h, c < i, f < n, g < m, h < l, i < j, i < k
fn select_206([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < b {
        select_201([a, d, f, g, h, i, b, j, k, l, m, n])
    } else {
        select_205([a, b, c, d, e, f, g, h, l, m, n, i])
    }
}
/// n = 10, i = 2, a < c, a < j, b < d, b < j, c < i, d < e, d < f, d < g, d < h
fn select_207([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_22([a, e, f, g, h])
    } else {
        select_27([c, b, d, j, i])
    }
}
/// n = 11, i = 2, a < k, b < d, b < j, c < e, c < j, c < k, e < f, e < g, e < h, e < i
fn select_208([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_207([a, c, b, e, f, g, h, i, d, k])
    } else {
        select_174([b, c, a, d, e, f, g, h, i, j])
    }
}
/// n = 11, i = 2, b < e, b < k, c < d, c < f, c < k, f < g, f < h, f < i, f < j
fn select_209([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_160([b, c, e, d, f, g, h, i, j, a, k])
    } else {
        select_208([a, b, c, e, f, g, h, i, j, k, d])
    }
}
/// n = 13, i = 3, a < d, a < f, a < i, b < c, b < e, b < i, e < g, f < h, i < j, i < k, i < l, i < m
fn select_210([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if e < f {
        select_209([c, e, a, d, g, i, j, k, l, m, f])
    } else {
        select_209([d, f, b, c, h, i, j, k, l, m, e])
    }
}
/// n = 16, i = 3, a < d, a < f, b < c, b < e, b < g, e < i, f < j, g < h, g < k, g < l, g < m, k < p, l < o, m < n
fn select_211([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if g < a {
        select_206([c, e, g, h, i, k, l, m, a, d, f, n, o, p])
    } else {
        select_210([a, b, c, d, e, f, i, j, g, h, k, l, m])
    }
}
/// n = 6, i = 1, c < d, c < e, c < f
fn select_212([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_24([a, c, d, e, f, b])
    } else {
        select_24([b, c, d, e, f, a])
    }
}
/// n = 11, i = 2, a < c, a < d, b < e, b < f, e < k, f < g, f < h, f < i, f < j
fn select_213([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_155([e, f, g, h, i, j, a, k])
    } else {
        select_174([a, b, c, d, f, g, h, i, j, e])
    }
}
/// n = 9, i = 1, a < g, a < h, a < i, b < c, b < d, b < e, b < f
fn select_214([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_4([b, g, h, i])
    } else {
        select_22([a, c, d, e, f])
    }
}
/// n = 12, i = 2, a < c, a < d, b < e, b < f, e < k, e < l, f < g, f < h, f < i, f < j
fn select_215([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < a {
        select_214([e, f, g, h, i, j, a, k, l])
    } else {
        select_174([a, b, c, d, f, g, h, i, j, e])
    }
}
/// n = 12, i = 2, a < d, a < e, b < c, b < f, b < g, f < l, g < h, g < i, g < j, g < k
fn select_216([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if c < f {
        select_213([a, b, d, e, c, g, h, i, j, k, f])
    } else {
        select_215([a, b, d, e, f, g, h, i, j, k, c, l])
    }
}
/// n = 9, i = 2, a < c, a < i, b < d, b < i, c < h, d < e, d < f, d < g
fn select_217([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_4([a, e, f, g])
    } else {
        select_27([c, b, d, i, h])
    }
}
/// n = 11, i = 2, a < c, b < d, b < e, c < k, d < i, d < j, e < f, e < g, e < h
fn select_218([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_6([d, e, f, g, h, a, i, j])
    } else {
        select_217([a, b, c, e, f, g, h, k, d])
    }
}
/// n = 10, i = 3, a < d, a < e, b < d, b < f, c < e, c < f, e < j, f < g, f < h, f < i
fn select_219([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_4([a, g, h, i])
    } else {
        select_90([b, c, d, e, j, f])
    }
}
/// n = 11, i = 3, a < e, b < d, b < f, c < e, c < f, c < j, d < j, e < k, f < g, f < h, f < i
fn select_220([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_12([d, c, a, f, g, h, i, j])
    } else {
        select_219([a, b, c, d, e, f, g, h, i, k])
    }
}
/// n = 12, i = 3, a < f, b < d, b < e, b < g, c < e, c < f, c < g, e < k, f < l, g < h, g < i, g < j
fn select_221([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < d {
        select_218([a, b, f, e, g, h, i, j, d, k, l])
    } else {
        select_220([a, b, c, d, f, g, h, i, j, e, l])
    }
}
/// n = 13, i = 3, a < f, b < d, b < e, b < g, c < e, c < f, c < g, e < l, f < m, g < h, g < i, g < j, g < k
fn select_222([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if h < a {
        select_156([d, e, g, h, i, j, k, l])
    } else {
        select_221([a, b, c, d, e, f, g, i, j, k, l, m])
    }
}
/// n = 13, i = 3, b < d, b < g, b < h, c < e, c < g, c < h, e < f, g < m, h < i, h < j, h < k, h < l
fn select_223([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if e < a {
        select_216([e, b, d, a, f, g, h, i, j, k, l, m])
    } else {
        select_222([a, b, c, d, g, e, h, i, j, k, l, m, f])
    }
}
/// n = 14, i = 4, a < e, a < g, a < j, b < d, b < f, b < j, c < f, c < g, c < j, f < h, g < i, j < k, j < l, j < m, j < n
fn select_224([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if f < a {
        select_212([d, h, a, e, g, j])
    } else {
        select_223([e, b, c, d, g, i, f, j, k, l, m, n, h])
    }
}
/// n = 17, i = 4, a < e, a < g, b < d, b < f, b < h, c < f, c < g, c < h, f < j, g < k, h < i, h < l, h < m, h < n, l < q, m < p, n < o
fn select_225([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if h < a {
        select_206([d, f, h, i, j, l, m, n, a, e, g, o, p, q])
    } else {
        select_224([a, b, c, d, e, f, g, j, k, h, i, l, m, n])
    }
}
/// n = 17, i = 4, a < e, b < d, b < h, b < i, c < f, c < h, c < i, f < g, h < k, i < j, i < l, i < m, i < n, l < q, m < p, n < o
fn select_226([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if f < a {
        select_211([f, b, d, g, h, a, i, j, k, e, l, m, n, o, p, q])
    } else {
        select_225([a, b, c, d, e, h, f, i, j, k, g, l, m, n, o, p, q])
    }
}
/// n = 9, i = 2, a < c, a < i, b < d, b < i, d < e, d < f, d < g, d < h
fn select_227([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_22([a, e, f, g, h])
    } else {
        select_11([c, b, d, i])
    }
}
/// n = 9, i = 2, b < i, c < d, c < i, d < e, d < f, d < g, d < h
fn select_228([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_128([a, c, b, d, e, f, g, h])
    } else {
        select_227([b, c, a, d, e, f, g, h, i])
    }
}
/// n = 11, i = 3, b < d, b < g, c < e, c < g, e < f, g < h, g < i, g < j, g < k
fn select_229([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_228([a, d, c, g, h, i, j, k, e])
    } else {
        select_175([a, e, b, f, g, h, i, j, k, d])
    }
}
/// n = 8, i = 2, a < g, a < h, b < f, b < h, c < d, c < f, c < g, d < e
fn select_230([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_137([a, c, d, b, e, h, g])
    } else {
        select_137([b, c, d, a, e, h, f])
    }
}
/// n = 9, i = 3, a < f, a < i, b < f, b < g, b < i, c < d, c < i, d < e, d < g, f < h
fn select_231([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_73([a, e, b, g])
    } else {
        select_137([b, c, d, f, e, h, i])
    }
}
/// n = 10, i = 3, a < e, a < j, b < g, b < i, b < j, c < d, c < g, c < j, d < i, e < f, g < h
fn select_232([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_230([a, d, b, g, h, i, j, e])
    } else {
        select_231([b, c, a, e, f, g, d, h, j])
    }
}
/// n = 10, i = 3, a < f, a < j, b < e, b < h, b < j, c < d, c < h, c < j, f < g, h < i
fn select_233([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_232([a, b, c, d, f, g, h, i, e, j])
    } else {
        select_232([a, c, b, e, f, g, h, i, d, j])
    }
}
/// n = 7, i = 2, a < f, a < g, b < e, b < g, c < d, c < e, c < f
fn select_234([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_90([c, a, d, b, g, f])
    } else {
        select_90([c, b, d, a, g, e])
    }
}
/// n = 8, i = 3, a < d, a < h, b < c, b < g, c < e, c < h, d < f, d < g
fn select_235([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_11([e, a, d, h])
    } else {
        select_11([f, b, c, g])
    }
}
/// n = 9, i = 3, a < d, a < i, b < c, b < e, c < h, d < g, e < f, e < h, e < i
fn select_236([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_234([a, c, e, f, h, i, d])
    } else {
        select_235([a, b, e, d, f, g, c, i])
    }
}
/// n = 6, i = 2, a < c, b < d, d < e, d < f
fn select_237([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < a {
        select_3([a, e, f])
    } else {
        select_10([c, b, d])
    }
}
/// n = 8, i = 3, a < d, b < c, b < g, b < h, c < f, d < e, d < g, d < h
fn select_238([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < c {
        select_11([e, b, g, h])
    } else {
        select_237([c, a, f, d, g, h])
    }
}
/// n = 10, i = 3, a < c, a < j, b < d, c < f, d < e, d < g, d < j, g < h, g < i
fn select_239([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_18([e, g, a, h, i])
    } else {
        select_238([b, a, c, d, e, f, g, j])
    }
}
/// n = 10, i = 3, a < d, a < j, b < c, b < e, d < g, e < f, e < h, e < j, h < i
fn select_240([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < h {
        select_236([a, b, c, d, e, f, g, h, j])
    } else {
        select_239([a, b, d, e, f, g, h, c, i, j])
    }
}
/// n = 11, i = 3, a < e, a < k, b < f, b < j, b < k, c < d, c < g, c < k, f < i, g < h, g < j
fn select_241([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < g {
        select_233([b, a, c, d, e, f, i, g, h, k])
    } else {
        select_240([b, c, d, f, g, h, i, a, e, j])
    }
}
/// n = 7, i = 2, a < c, a < g, b < d, b < g, d < e, d < f
fn select_242([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_3([a, e, f])
    } else {
        select_11([c, b, d, g])
    }
}
/// n = 7, i = 2, a < f, a < g, b < d, b < e, c < e, c < f, c < g
fn select_243([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if b < a {
        select_73([a, d, c, e])
    } else {
        select_27([b, c, f, g, d])
    }
}
/// n = 8, i = 2, a < h, b < d, b < g, c < e, c < g, c < h, e < f
fn select_244([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_242([b, c, d, e, a, f, g])
    } else {
        select_243([a, b, c, d, g, e, h])
    }
}
/// n = 9, i = 3, a < d, a < i, b < c, b < g, b < h, c < f, c < i, d < e, d < g, d < h
fn select_245([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_11([f, a, d, i])
    } else {
        select_18([e, b, c, g, h])
    }
}
/// n = 10, i = 3, a < e, a < i, a < j, b < c, b < d, b < h, c < j, d < f, d < i, e < g, e < h
fn select_246([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < e {
        select_243([c, d, a, f, i, e, j])
    } else {
        select_245([a, b, d, e, g, f, c, h, i])
    }
}
/// n = 10, i = 3, a < d, a < e, a < i, b < c, b < f, b < j, d < j, e < h, f < g, f < i
fn select_247([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < e {
        select_244([c, f, a, g, d, j, i, e])
    } else {
        select_246([b, a, d, e, f, h, g, i, c, j])
    }
}
/// n = 7, i = 3, a < d, a < g, b < e, b < g, c < e, c < g, e < f
fn select_248([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < d {
        select_72([a, e, f, g])
    } else {
        select_44([d, b, c, g])
    }
}
/// n = 8, i = 3, a < h, b < d, b < g, b < h, c < e, c < h, e < f, e < g
fn select_249([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_176([b, e, a, f, d, g])
    } else {
        select_248([b, a, c, d, e, f, h])
    }
}
/// n = 9, i = 3, a < e, a < i, b < c, b < d, b < h, d < f, d < i, e < g, e < h
fn select_250([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < e {
        select_79([c, a, d, f, i, e])
    } else {
        select_245([a, b, d, e, g, f, c, h, i])
    }
}
/// n = 10, i = 4, a < e, a < g, b < d, b < f, b < j, c < f, c < g, f < i, g < h, g < j
fn select_251([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_249([e, b, c, d, g, h, j, f])
    } else {
        select_250([a, b, d, f, g, i, h, j, e])
    }
}
/// n = 11, i = 4, a < d, a < k, b < e, b < h, b < k, c < f, c < h, e < j, f < g, f < j, f < k, h < i
fn select_252([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_247([b, f, g, e, h, a, d, i, k, j])
    } else {
        select_251([a, b, c, e, d, h, f, g, i, k])
    }
}
/// n = 12, i = 4, a < e, a < l, b < d, b < i, b < l, c < f, c < i, f < g, f < h, f < l, h < j, i < k
fn select_253([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < d {
        select_241([a, b, f, g, e, i, h, j, k, d, l])
    } else {
        select_252([a, b, c, e, d, f, g, i, k, h, l])
    }
}
/// n = 15, i = 4, a < e, a < l, b < d, b < i, b < l, c < f, c < i, c < l, f < g, f < h, h < j, i < k, l < m, l < n, l < o
fn select_254([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if l < f {
        select_229([d, a, c, e, i, k, l, f, m, n, o])
    } else {
        select_253([a, b, c, d, e, f, g, h, i, j, k, l])
    }
}
/// n = 6, i = 3, a < f, b < e, b < f, c < d, c < f
fn select_255([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < e {
        select_92([a, d, b, e, f])
    } else {
        select_92([a, e, c, d, f])
    }
}
/// n = 6, i = 2, b < f, c < d, c < f, d < e
fn select_256([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < a {
        select_27([b, d, a, e, f])
    } else {
        select_92([a, b, c, f, d])
    }
}
/// n = 8, i = 3, a < e, a < h, b < f, b < h, c < d, c < f, c < h, f < g
fn select_257([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_255([b, a, c, d, e, h])
    } else {
        select_256([d, a, b, f, g, h])
    }
}
/// n = 9, i = 3, a < e, a < i, b < d, b < h, b < i, c < f, c < i, f < g, f < h
fn select_258([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_39([b, f, g, d, a, e, h])
    } else {
        select_257([b, c, a, e, d, f, g, i])
    }
}
/// n = 6, i = 2, a < f, b < d, b < e, c < d, c < e, c < f
fn select_259([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_10([b, c, f])
    } else {
        select_11([a, c, d, e])
    }
}
/// n = 6, i = 2, b < e, b < f, c < d, c < e, c < f
fn select_260([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < a {
        select_27([d, b, e, f, a])
    } else {
        select_259([a, b, c, e, f, d])
    }
}
/// n = 7, i = 3, a < f, a < g, b < e, b < f, b < g, c < d, c < f, c < g
fn select_261([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < e {
        select_259([d, a, b, f, g, e])
    } else {
        select_259([e, a, c, f, g, d])
    }
}
/// n = 10, i = 4, a < g, a < j, b < e, b < i, c < d, c < g, c < j, e < f, e < j, g < h, g < i
fn select_262([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < e {
        select_260([d, b, g, h, e, i])
    } else {
        select_261([a, c, e, f, d, g, j])
    }
}
/// n = 11, i = 4, a < d, a < h, a < k, b < g, b < h, b < k, c < e, c < g, e < f, e < k, g < i, h < j
fn select_263([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < h {
        select_258([e, a, b, d, f, g, i, h, k])
    } else {
        select_262([b, c, a, d, e, f, h, j, g, k])
    }
}
/// n = 8, i = 3, a < f, a < h, b < f, b < g, b < h, c < d, c < h, d < e, d < g
fn select_264([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_73([a, e, b, g])
    } else {
        select_90([b, c, f, d, e, h])
    }
}
/// n = 8, i = 3, a < d, a < h, b < e, b < h, c < e, c < h, e < f, e < g
fn select_265([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_44([d, b, c, h])
    } else {
        select_27([a, e, f, g, h])
    }
}
/// n = 8, i = 3, a < g, a < h, b < d, b < h, c < e, c < h, e < f, e < g
fn select_266([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_62([b, e, f, d, a, g])
    } else {
        select_265([b, a, c, d, e, f, g, h])
    }
}
/// n = 10, i = 4, a < g, a < j, b < d, b < h, b < j, c < e, c < g, d < f, e < h, e < j, g < i
fn select_267([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < d {
        select_264([e, b, a, g, i, h, d, j])
    } else {
        select_266([a, d, c, f, e, h, j, g])
    }
}
/// n = 7, i = 3, a < e, a < g, b < c, b < d, d < g, e < f
fn select_268([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < e {
        select_92([c, d, a, g, e])
    } else {
        select_90([e, b, f, d, g, c])
    }
}
/// n = 7, i = 4, a < d, b < f, c < e, e < g, f < g
fn select_269([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < d {
        select_96([a, e, b, f, d, g])
    } else {
        select_71([c, d, b, f, e])
    }
}
/// n = 10, i = 5, a < g, a < h, b < e, c < d, c < g, d < f, e < h, e < j, g < j, h < i
fn select_270([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < f {
        select_268([e, c, d, g, h, i, j])
    } else {
        select_269([d, a, b, f, e, g, j])
    }
}
/// n = 6, i = 3, b < e, c < d, c < f, e < f
fn select_271([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if e < a {
        select_19([c, e, a, d, f])
    } else {
        select_71([a, b, c, d, e])
    }
}
/// n = 8, i = 4, a < d, b < f, c < e, c < g, e < h, f < g, f < h
fn select_272([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < a {
        select_62([a, c, g, d, e, h])
    } else {
        select_271([d, b, c, e, f, g])
    }
}
/// n = 10, i = 5, a < h, b < f, c < d, c < e, d < i, e < g, f < h, f < i, h < j
fn select_273([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < d {
        select_270([a, b, c, e, f, g, d, h, j, i])
    } else {
        select_272([e, b, d, g, a, f, i, h])
    }
}
/// n = 11, i = 5, a < i, a < k, b < d, b < e, b < k, c < f, e < g, f < h, f < i, h < k, i < j
fn select_274([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < d {
        select_267([a, b, f, e, h, g, i, d, j, k])
    } else {
        select_273([a, c, b, d, e, f, g, i, h, j])
    }
}
/// n = 6, i = 3, a < e, b < c, b < d, e < f
fn select_275([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if e < c {
        select_19([b, e, f, d, c])
    } else {
        select_44([d, a, c, e])
    }
}
/// n = 7, i = 3, a < c, a < d, b < e, e < f, e < g
fn select_276([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < c {
        select_107([a, e, f, g, d])
    } else {
        select_275([b, a, c, d, e, g])
    }
}
/// n = 7, i = 3, a < d, b < c, b < g, c < f, d < e, d < g
fn select_277([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < d {
        select_10([f, a, d])
    } else {
        select_11([e, b, c, g])
    }
}
/// n = 8, i = 3, a < c, a < h, b < d, c < g, d < e, d < f, d < h
fn select_278([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < c {
        select_73([e, f, a, h])
    } else {
        select_277([b, a, c, d, f, g, h])
    }
}
/// n = 8, i = 3, a < h, b < d, c < e, e < f, e < g, e < h
fn select_279([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < a {
        select_276([b, c, a, d, e, f, g])
    } else {
        select_278([a, c, b, e, f, g, d, h])
    }
}
/// n = 9, i = 3, a < c, a < i, b < d, c < f, d < e, d < g, d < i, g < h
fn select_280([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < c {
        select_42([e, a, g, h, i])
    } else {
        select_277([b, a, c, d, e, f, i])
    }
}
/// n = 8, i = 3, a < c, b < d, c < e, d < f, f < g, f < h
fn select_281([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < f {
        select_64([b, c, e, d])
    } else {
        select_11([a, f, g, h])
    }
}
/// n = 8, i = 4, a < f, b < f, b < h, c < d, d < e, e < h, f < g
fn select_282([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_44([a, b, e, h])
    } else {
        select_64([c, f, g, d])
    }
}
/// n = 9, i = 4, a < f, b < f, b < h, c < d, d < e, d < h, f < g, h < i
fn select_283([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if h < e {
        select_281([a, c, f, d, g, h, e, i])
    } else {
        select_282([a, b, c, d, e, f, g, h])
    }
}
/// n = 10, i = 4, a < f, a < j, b < f, b < g, c < d, c < g, d < e, f < i, g < h, g < j
fn select_284([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < d {
        select_280([a, c, f, g, h, i, d, e, j])
    } else {
        select_283([a, b, c, d, e, f, i, g, h])
    }
}
/// n = 11, i = 4, a < f, a < k, b < f, b < g, c < d, c < g, d < e, f < j, g < h, g < i, g < k
fn select_285([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < f {
        select_279([a, d, b, e, g, h, i, k])
    } else {
        select_284([a, b, c, d, e, f, g, i, j, k])
    }
}
/// n = 7, i = 2, a < g, b < f, b < g, c < d, c < f, d < e
fn select_286([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_27([b, d, a, e, f])
    } else {
        select_78([a, b, c, f, d, g])
    }
}
/// n = 6, i = 3, a < d, b < e, c < e, e < f
fn select_287([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if e < d {
        select_10([a, e, f])
    } else {
        select_70([b, c, d])
    }
}
/// n = 8, i = 4, a < f, b < e, c < f, c < h, d < f, d < h, e < h, f < g
fn select_288([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_287([b, c, d, e, f, g])
    } else {
        select_44([a, c, d, h])
    }
}
/// n = 9, i = 4, a < e, b < g, b < i, c < f, c < g, d < f, d < g, f < i, g < h
fn select_289([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < e {
        select_286([a, f, b, g, h, i, e])
    } else {
        select_288([b, a, c, d, e, g, h, f])
    }
}
/// n = 9, i = 4, a < g, a < i, b < f, b < g, c < d, c < f, d < e, f < i, g < h
fn select_290([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < g {
        select_93([a, d, b, e, f, i, g])
    } else {
        select_90([g, c, h, f, i, d])
    }
}
/// n = 11, i = 5, a < h, a < j, b < f, b < j, c < d, c < e, d < g, e < j, f < h, h < i, j < k
fn select_291([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_289([d, a, b, e, g, f, j, k, h])
    } else {
        select_290([a, f, c, d, g, e, h, i, j])
    }
}
/// n = 12, i = 5, a < h, a < i, b < f, b < i, c < d, c < e, c < i, e < g, f < h, f < l, h < j, i < k, i < l
fn select_292([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if i < d {
        select_285([f, a, c, e, g, h, i, d, k, j, l])
    } else {
        select_291([a, b, c, e, d, f, g, h, j, i, k])
    }
}
/// n = 12, i = 5, a < i, a < j, b < d, b < e, b < j, c < f, c < j, e < h, f < g, f < i, i < k, j < l
fn select_293([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < j {
        select_274([a, b, c, d, e, f, h, g, i, k, j])
    } else {
        select_292([a, c, b, d, e, f, h, i, j, k, l, g])
    }
}
/// n = 13, i = 5, a < i, a < j, a < m, b < d, b < e, b < j, c < f, c < j, e < h, e < m, f < g, f < i, f < m, i < k, j < l
fn select_294([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if m < d {
        select_263([f, a, b, g, e, h, j, i, l, k, m])
    } else {
        select_293([a, b, c, d, e, f, g, h, i, j, k, l])
    }
}
/// n = 7, i = 3, a < f, a < g, b < f, b < g, c < d, c < g, d < e
fn select_295([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_83([a, b, e])
    } else {
        select_90([b, c, f, d, e, g])
    }
}
/// n = 9, i = 3, a < d, a < i, b < e, b < g, b < i, c < e, c < g, c < i, d < f, g < h
fn select_296([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < d {
        select_42([e, a, g, h, i])
    } else {
        select_295([b, c, a, d, f, e, i])
    }
}
/// n = 12, i = 3, a < f, a < g, b < d, b < h, c < f, c < g, c < h, d < e, g < l, h < i, h < j, h < k
fn select_297([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < a {
        select_128([d, c, e, h, a, i, j, k])
    } else {
        select_296([b, a, c, d, f, e, g, l, h])
    }
}
/// n = 11, i = 4, a < f, a < i, b < f, b < h, c < d, d < e, d < h, d < i, f < g, h < j, i < k
fn select_298([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < i {
        select_283([a, b, c, d, e, f, g, h, j])
    } else {
        select_283([b, a, c, d, e, f, g, i, k])
    }
}
/// n = 11, i = 3, a < c, a < g, b < d, b < g, c < e, d < f, f < h, g < i, g < j, g < k
fn select_299([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < d {
        select_12([c, b, e, g, i, j, k, d])
    } else {
        select_217([d, a, f, g, i, j, k, h, c])
    }
}
/// n = 6, i = 2, a < d, b < c, c < e, d < f
fn select_300([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if c < d {
        select_10([a, c, e])
    } else {
        select_10([b, d, f])
    }
}
/// n = 7, i = 3, a < c, b < d, c < e, d < f, f < g
fn select_301([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < d {
        select_10([e, b, d])
    } else {
        select_72([a, f, g, c])
    }
}
/// n = 10, i = 4, a < e, a < h, b < e, b < g, c < d, d < g, d < h, e < f, g < i, h < j
fn select_302([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < e {
        select_300([a, b, g, h, i, j])
    } else {
        select_301([b, c, e, d, f, h, j])
    }
}
/// n = 14, i = 4, a < e, a < h, a < i, b < e, b < g, b < i, c < d, c < i, d < g, d < h, e < f, g < j, h < k, i < l, i < m, i < n
fn select_303([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < g {
        select_299([b, c, e, d, f, h, i, k, l, m, n])
    } else {
        select_302([a, b, c, d, e, f, g, h, j, k])
    }
}
/// n = 15, i = 4, a < f, a < i, a < j, b < f, b < h, b < j, c < d, c < j, d < e, d < h, d < i, f < g, h < k, i < l, j < m, j < n, j < o
fn select_304([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if e < j {
        select_298([a, b, c, d, e, f, g, h, i, k, l])
    } else {
        select_303([a, b, c, d, f, g, h, i, j, k, l, m, n, o])
    }
}
/// n = 15, i = 4, a < g, a < j, a < k, b < d, b < g, b < k, c < e, c < h, c < k, d < h, e < f, e < j, g < i, j < l, k < m, k < n, k < o
fn select_305([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if d < e {
        select_297([d, a, c, g, i, h, e, k, m, n, o, f])
    } else {
        select_304([a, b, c, e, f, g, i, d, j, k, h, l, m, n, o])
    }
}
/// n = 4, i = 2, c < d
fn select_306([a, b, c, d]: [usize; 4]) -> usize {
    if a < b {
        select_64([a, c, d, b])
    } else {
        select_64([b, c, d, a])
    }
}
/// n = 7, i = 3, a < f, b < d, b < e, c < e, c < f, f < g
fn select_307([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < d {
        select_84([b, a, e, f, g])
    } else {
        select_306([a, d, c, e])
    }
}
/// n = 9, i = 3, a < d, b < f, b < h, b < i, c < e, c < f, e < h, e < i, f < g
fn select_308([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_86([b, e, a, f, d, g, h, i])
    } else {
        select_307([b, a, c, d, e, f, g])
    }
}
/// n = 9, i = 2, a < c, a < h, a < i, b < d, b < h, b < i, c < g, d < e, d < f
fn select_309([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_27([c, b, h, i, g])
    } else {
        select_151([a, d, e, f, h, i])
    }
}
/// n = 7, i = 2, a < c, b < d, c < g, d < e, d < f
fn select_310([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_3([a, e, f])
    } else {
        select_72([b, c, g, d])
    }
}
/// n = 7, i = 3, a < e, b < d, c < e, c < g, d < g, e < f
fn select_311([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < e {
        select_44([a, c, d, g])
    } else {
        select_10([b, e, f])
    }
}
/// n = 8, i = 3, a < f, b < d, b < e, c < e, c < f, e < g, f < h
fn select_312([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < d {
        select_310([a, b, f, e, d, g, h])
    } else {
        select_311([a, b, c, d, f, h, e])
    }
}
/// n = 10, i = 3, a < d, a < j, b < f, b < h, b < i, c < e, c < f, e < h, e < i, e < j, f < g
fn select_313([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_309([b, e, f, a, d, j, g, h, i])
    } else {
        select_312([b, a, c, d, e, f, j, g])
    }
}
/// n = 10, i = 3, b < j, c < f, c < h, c < i, d < e, d < f, e < h, e < i, e < j, f < g
fn select_314([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_308([a, c, d, b, e, f, g, h, i])
    } else {
        select_313([b, c, d, a, e, f, g, h, i, j])
    }
}
/// n = 8, i = 3, a < c, b < d, c < f, d < e, d < g, g < h
fn select_315([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if g < a {
        select_11([e, g, a, h])
    } else {
        select_277([b, a, c, d, e, f, g])
    }
}
/// n = 6, i = 1, b < f, c < d, c < e
fn select_316([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_27([a, c, d, e, b])
    } else {
        select_151([b, c, d, e, a, f])
    }
}
/// n = 10, i = 3, a < c, a < i, a < j, b < d, c < f, d < e, d < g, d < i, d < j, g < h
fn select_317([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < c {
        select_316([e, g, a, i, j, h])
    } else {
        select_238([b, a, c, d, e, f, i, j])
    }
}
/// n = 10, i = 3, a < d, a < i, a < j, b < c, b < e, c < g, d < h, e < f, e < i, e < j
fn select_318([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < e {
        select_315([a, b, d, c, g, h, e, f])
    } else {
        select_317([a, b, d, e, f, h, c, g, i, j])
    }
}
/// n = 11, i = 3, a < d, a < g, b < c, b < g, c < e, d < f, g < h, g < i, g < j, g < k
fn select_319([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < d {
        select_227([c, a, e, g, h, i, j, k, d])
    } else {
        select_227([d, b, f, g, h, i, j, k, c])
    }
}
/// n = 13, i = 3, a < d, a < i, a < m, b < c, b < e, b < i, c < g, d < h, e < f, e < m, i < j, i < k, i < l
fn select_320([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if e < i {
        select_318([a, b, c, d, e, f, g, h, i, m])
    } else {
        select_319([a, b, c, d, g, h, i, e, j, k, l])
    }
}
/// n = 16, i = 5, a < h, a < k, a < l, b < f, b < k, c < d, c < e, c < l, d < i, e < g, e < k, f < h, f < i, f < l, h < j, k < p, l < m, l < n, l < o
fn select_321([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < f {
        select_314([g, d, a, b, f, k, p, h, l, i])
    } else {
        select_320([a, c, d, h, e, g, i, j, l, m, n, o, k])
    }
}
/// n = 16, i = 5, a < i, a < k, a < l, b < d, b < e, b < l, c < f, c < k, e < h, e < k, f < g, f < i, f < l, i < j, k < p, l < m, l < n, l < o
fn select_322([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if g < d {
        select_305([a, f, b, g, e, h, i, d, j, k, l, p, m, n, o])
    } else {
        select_321([a, c, b, d, e, f, h, i, g, j, k, l, m, n, o, p])
    }
}
/// n = 16, i = 5, a < f, a < j, b < e, b < m, c < i, c < j, c < m, d < g, d < j, g < h, g < i, g < m, i < k, j < l, m < n, m < o, m < p
fn select_323([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_294([c, a, d, f, b, g, h, e, i, j, k, l, m])
    } else {
        select_322([c, b, d, e, a, g, h, f, i, k, j, m, n, o, p, l])
    }
}
/// n = 16, i = 5, a < f, b < e, b < m, c < i, c < k, c < m, d < g, d < i, g < h, g < k, g < m, i < j, k < l, m < n, m < o, m < p
fn select_324([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if i < a {
        select_254([b, g, c, h, e, i, j, a, k, f, l, m, n, o, p])
    } else {
        select_323([a, b, c, d, e, f, g, h, k, i, l, j, m, n, o, p])
    }
}
/// n = 18, i = 5, a < f, b < e, c < i, c < k, c < l, d < g, d < i, g < h, g < k, g < l, i < j, k < n, l < m, l < o, l < p, o < r, p < q
fn select_325([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if l < b {
        select_226([a, g, c, h, f, i, j, k, l, m, n, b, o, p, q, r, e])
    } else {
        select_324([a, b, c, d, e, f, g, h, i, j, k, n, l, m, o, p])
    }
}
/// n = 18, i = 5, a < f, b < e, c < i, c < o, d < g, d < i, g < h, g < j, g < o, i < l, j < k, j < m, j < n, m < q, n < p, o < r
fn select_326([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if j < c {
        select_197([a, b, g, h, e, f, j, k, m, n, c, p, q, i, o, r, l])
    } else {
        select_325([a, b, c, d, e, f, g, h, i, l, o, j, k, r, m, n, p, q])
    }
}
/// n = 18, i = 5, a < f, b < e, c < o, d < g, d < h, g < j, h < i, h < k, h < o, k < l, k < m, k < n, m < q, n < p, o < r
fn select_327([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if g < c {
        select_189([a, b, g, h, i, j, e, f, c, k, l, m, n, p, q, o, r])
    } else {
        select_326([a, b, c, d, e, f, h, i, g, k, l, j, m, n, o, p, q, r])
    }
}
/// n = 5, i = 2, b < e, c < d
fn select_328([a, b, c, d, e]: [usize; 5]) -> usize {
    if b < c {
        select_73([a, e, c, d])
    } else {
        select_73([a, d, b, e])
    }
}
/// n = 7, i = 3, a < g, b < e, c < d, c < f, f < g
fn select_329([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_328([f, b, d, a, e])
    } else {
        select_114([b, a, c, e, f, d, g])
    }
}
/// n = 7, i = 2, a < f, a < g, b < d, b < e, c < d, c < e, c < f, c < g
fn select_330([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_11([b, c, f, g])
    } else {
        select_11([a, c, d, e])
    }
}
/// n = 9, i = 3, a < d, a < g, a < h, a < i, b < c, b < e, c < i, d < f, e < g, e < h
fn select_331([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < c {
        select_242([d, b, f, e, g, h, c])
    } else {
        select_330([c, e, a, g, h, d, i])
    }
}
/// n = 9, i = 3, a < d, a < g, b < c, b < g, b < i, c < f, d < e, d < i, g < h
fn select_332([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_90([c, a, f, g, h, d])
    } else {
        select_150([d, b, e, g, h, c, i])
    }
}
/// n = 10, i = 3, a < g, a < j, b < e, b < j, c < d, c < g, c < i, c < j, d < f, e < i, g < h
fn select_333([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < a {
        select_331([c, b, e, d, a, f, g, j, i])
    } else {
        select_332([a, c, d, b, e, f, g, h, j])
    }
}
/// n = 10, i = 3, a < e, b < g, b < j, c < f, c < j, d < g, d < i, d < j, f < i, g < h
fn select_334([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < d {
        select_329([b, c, a, e, f, d, g])
    } else {
        select_333([b, c, d, a, f, e, g, h, i, j])
    }
}
/// n = 10, i = 3, a < d, a < e, b < f, c < e, c < f, f < g, f < h, f < i, f < j
fn select_335([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_22([a, g, h, i, j])
    } else {
        select_102([d, b, c, e, f])
    }
}
/// n = 11, i = 3, a < d, b < f, b < k, c < e, c < f, e < k, f < g, f < h, f < i, f < j
fn select_336([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_207([e, b, a, f, g, h, i, j, d, k])
    } else {
        select_335([a, b, c, d, e, f, g, h, i, j])
    }
}
/// n = 13, i = 3, a < e, b < g, c < f, c < h, d < g, d < h, d < l, f < l, g < m, h < i, h < j, h < k
fn select_337([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if b < h {
        select_334([a, b, c, d, e, f, g, m, l, h])
    } else {
        select_336([a, d, c, e, f, h, b, i, j, k, l])
    }
}
/// n = 7, i = 2, b < g, c < d, c < g, d < e, d < f
fn select_338([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < b {
        select_18([a, d, b, e, f])
    } else {
        select_52([a, b, c, d, g])
    }
}
/// n = 10, i = 3, a < e, a < j, b < f, b < i, b < j, c < d, c < f, c < j, e < i, f < g, f < h
fn select_339([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_338([d, a, b, f, g, h, j])
    } else {
        select_93([b, c, a, d, e, i, j])
    }
}
/// n = 13, i = 3, a < d, a < f, b < e, b < g, c < f, c < g, c < k, e < k, f < l, f < m, g < h, g < i, g < j
fn select_340([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if g < a {
        select_23([e, g, a, h, i, j, k])
    } else {
        select_339([b, c, a, d, e, f, l, m, k, g])
    }
}
/// n = 13, i = 3, a < d, a < f, a < g, b < e, b < h, c < f, c < g, c < h, c < l, e < l, g < m, h < i, h < j, h < k
fn select_341([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if a < b {
        select_82([d, b, c, f, e, g, m, h])
    } else {
        select_31([e, a, c, d, h, i, j, k, f, g, l])
    }
}
/// n = 14, i = 4, a < e, a < j, b < f, b < j, b < n, c < d, c < i, c < j, c < n, d < h, e < n, f < g, f < i, j < k, j < l, j < m
fn select_342([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if d < f {
        select_340([d, a, b, h, e, f, j, k, l, m, n, g, i])
    } else {
        select_341([f, a, c, g, e, i, d, j, k, l, m, n, h])
    }
}
/// n = 14, i = 4, a < g, a < j, b < f, b < j, b < n, c < d, c < e, c < j, c < n, e < h, f < i, g < n, j < k, j < l, j < m
fn select_343([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if d < f {
        select_337([e, d, a, b, h, g, f, j, k, l, m, n, i])
    } else {
        select_342([a, b, c, e, g, f, i, h, d, j, k, l, m, n])
    }
}
/// n = 7, i = 3, a < g, b < d, b < g, c < e, c < g, e < f
fn select_344([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_107([b, e, a, f, d])
    } else {
        select_248([b, a, c, d, e, f, g])
    }
}
/// n = 8, i = 3, a < g, a < h, b < e, b < h, c < d, c < f, c < h, f < g
fn select_345([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < f {
        select_344([a, b, c, e, d, f, h])
    } else {
        select_266([a, b, c, e, f, d, g, h])
    }
}
/// n = 8, i = 3, a < h, b < d, c < e, c < g, d < g, e < f, e < h
fn select_346([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_52([a, c, d, e, g])
    } else {
        select_80([a, b, e, f, d, h])
    }
}
/// n = 6, i = 3, a < f, b < e, c < e, c < f, d < e, d < f
fn select_347([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_44([b, c, d, f])
    } else {
        select_44([a, c, d, e])
    }
}
/// n = 8, i = 4, a < g, a < h, b < f, c < e, d < f, d < h, e < h, f < g
fn select_348([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_347([a, b, d, e, f, h])
    } else {
        select_92([a, c, f, e, g])
    }
}
/// n = 9, i = 4, a < e, b < g, c < f, c < i, d < f, d < g, f < h, g < i
fn select_349([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < e {
        select_346([a, b, c, g, f, h, i, e])
    } else {
        select_348([c, b, a, d, e, g, i, f])
    }
}
/// n = 10, i = 4, a < h, b < e, b < i, c < h, c < i, d < f, d < j, f < g, f < i, h < j
fn select_350([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_345([c, b, f, g, e, a, h, i])
    } else {
        select_349([b, c, d, a, e, f, h, g, j])
    }
}
/// n = 9, i = 4, a < g, a < h, b < f, b < h, c < d, c < f, c < g, d < e, h < i
fn select_351([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < g {
        select_290([a, b, c, d, e, f, h, i, g])
    } else {
        select_290([b, a, c, d, e, g, h, i, f])
    }
}
/// n = 9, i = 4, a < e, a < h, b < e, b < g, c < d, c < i, d < g, d < h, e < f, e < i
fn select_352([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < d {
        select_11([f, c, d, i])
    } else {
        select_19([a, b, g, h, e])
    }
}
/// n = 11, i = 5, a < e, a < k, b < f, b < j, c < f, c < i, d < e, d < h, d < k, e < i, e < j, f < g, f < h, f < k
fn select_353([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < e {
        select_102([g, a, d, h, k])
    } else {
        select_352([b, c, a, e, f, h, i, j, k])
    }
}
/// n = 9, i = 4, a < h, b < g, b < h, c < f, c < h, d < e, e < f, e < g, h < i
fn select_354([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < e {
        select_132([b, c, d, e, h, i, f, g])
    } else {
        select_328([a, b, c, f, g])
    }
}
/// n = 11, i = 5, a < g, a < j, b < g, b < i, c < f, c < k, d < e, d < f, d < k, f < i, f < j, g < h, g < k
fn select_355([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < e {
        select_353([c, a, b, d, f, g, h, e, i, j, k])
    } else {
        select_354([e, a, b, c, f, i, j, g, h])
    }
}
/// n = 11, i = 5, a < e, a < k, b < g, b < j, c < g, c < i, d < f, d < k, f < i, f < j, g < h, g < k
fn select_356([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_351([b, c, f, a, e, i, j, g, h])
    } else {
        select_355([b, c, d, a, e, f, g, h, i, j, k])
    }
}
/// n = 11, i = 5, a < f, a < k, b < g, b < k, c < h, c < j, d < e, d < h, g < j, h < i, h < k
fn select_357([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < g {
        select_350([e, a, b, c, f, h, i, g, k, j])
    } else {
        select_356([a, c, d, b, f, g, h, i, e, j, k])
    }
}
/// n = 15, i = 5, a < e, b < g, b < k, c < f, c < k, c < o, d < h, d < j, f < j, g < o, h < i, h < k, h < o, k < l, k < m, k < n
fn select_358([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if h < a {
        select_343([b, c, h, i, a, f, g, e, j, k, l, m, n, o])
    } else {
        select_357([b, c, d, a, e, g, f, h, i, j, k])
    }
}
/// n = 9, i = 2, a < d, a < i, b < c, b < e, b < i, d < h, e < f, e < g
fn select_359([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_18([c, e, a, f, g])
    } else {
        select_150([b, a, c, d, h, e, i])
    }
}
/// n = 9, i = 3, a < i, b < d, b < g, c < e, c < h, d < h, e < f, e < g, e < i
fn select_360([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < b {
        select_316([f, a, b, d, g, i])
    } else {
        select_338([a, d, c, e, f, g, h])
    }
}
/// n = 10, i = 3, b < d, b < i, c < e, c < j, d < j, e < f, e < g, e < i, g < h
fn select_361([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_359([b, e, f, d, g, a, h, j, i])
    } else {
        select_360([a, b, c, d, e, f, i, j, g])
    }
}
/// n = 7, i = 3, a < f, a < g, b < e, c < d, d < f, e < g
fn select_362([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < d {
        select_92([a, c, e, d, g])
    } else {
        select_92([a, b, d, e, f])
    }
}
/// n = 9, i = 3, a < e, b < f, b < h, b < i, c < d, c < f, d < h, e < i, f < g
fn select_363([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < e {
        select_256([a, d, b, f, g, h])
    } else {
        select_362([b, a, c, d, e, h, i])
    }
}
/// n = 7, i = 2, a < c, b < d, b < e, d < g, e < f
fn select_364([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_27([e, d, a, g, f])
    } else {
        select_90([a, b, c, e, f, d])
    }
}
/// n = 7, i = 3, a < g, b < e, b < g, c < d, c < f, c < g, e < f
fn select_365([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_19([c, e, a, d, f])
    } else {
        select_45([a, b, c, d, e, g])
    }
}
/// n = 10, i = 4, a < e, b < f, b < j, c < d, c < g, c < j, d < i, e < j, f < g, f < i, g < h
fn select_366([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_364([a, c, e, d, g, h, i])
    } else {
        select_365([e, b, c, d, f, g, j])
    }
}
/// n = 10, i = 4, a < e, b < d, b < h, b < j, c < f, c < j, e < j, f < g, f < h, h < i
fn select_367([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < d {
        select_363([a, b, f, g, e, h, i, d, j])
    } else {
        select_366([a, c, b, d, e, f, h, i, g, j])
    }
}
/// n = 11, i = 4, a < f, a < j, b < d, b < h, b < k, c < e, c < h, c < k, e < g, f < k, h < i, h < j
fn select_368([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < e {
        select_361([d, a, c, f, h, i, e, g, j, k])
    } else {
        select_367([a, b, c, d, f, e, g, h, i, k])
    }
}
/// n = 8, i = 4, a < g, a < h, b < e, c < d, c < h, d < g, e < f, e < h
fn select_369([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < f {
        select_95([a, d, b, e, g, f, h])
    } else {
        select_92([a, f, c, d, h])
    }
}
/// n = 7, i = 3, b < e, b < g, c < d, c < f, d < g, e < f
fn select_370([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < d {
        select_96([a, c, b, e, d, f])
    } else {
        select_90([d, b, a, e, f, g])
    }
}
/// n = 9, i = 4, a < g, a < i, b < e, b < h, c < d, c < g, c < i, e < f, e < i, g < h
fn select_371([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < g {
        select_255([a, c, e, f, d, i])
    } else {
        select_370([d, a, b, e, g, h, i])
    }
}
/// n = 10, i = 4, a < j, b < g, b < i, c < g, c < i, c < j, d < e, d < h, e < f, e < i, e < j, g < h
fn select_372([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_369([c, d, a, b, e, f, g, j])
    } else {
        select_371([c, d, b, a, e, f, g, h, i])
    }
}
/// n = 10, i = 5, a < e, a < i, b < d, b < h, c < f, c < j, d < i, d < j, e < h, e < j, f < g, f < i
fn select_373([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_370([g, a, b, d, e, h, i])
    } else {
        select_268([c, b, h, d, f, g, j])
    }
}
/// n = 10, i = 5, a < d, a < i, b < e, b < j, c < f, c < h, d < j, e < h, e < i, f < g, f < j
fn select_374([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < h {
        select_373([b, a, c, d, e, f, g, i, j, h])
    } else {
        select_114([f, a, e, g, h, i, d])
    }
}
/// n = 11, i = 5, a < f, a < j, a < k, b < d, b < e, c < g, c < i, d < k, e < j, f < i, g < h, g < j, g < k
fn select_375([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < f {
        select_372([e, d, a, c, g, h, f, i, k, j])
    } else {
        select_374([b, a, c, e, f, g, h, i, d, j])
    }
}
/// n = 12, i = 5, a < d, a < f, b < e, b < j, b < l, c < g, c < i, e < i, f < l, g < h, g < j, g < l, j < k
fn select_376([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if j < d {
        select_368([a, g, b, h, e, f, i, j, k, d, l])
    } else {
        select_375([b, a, c, d, f, e, g, h, i, l, j])
    }
}
/// n = 8, i = 2, a < c, a < d, b < e, e < f, e < g, e < h
fn select_377([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_4([a, f, g, h])
    } else {
        select_73([c, d, b, e])
    }
}
/// n = 9, i = 2, a < i, b < d, c < e, c < i, e < f, e < g, e < h
fn select_378([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if b < a {
        select_377([b, c, a, d, e, f, g, h])
    } else {
        select_217([a, c, b, e, f, g, h, d, i])
    }
}
/// n = 9, i = 2, a < c, b < d, b < e, d < i, e < f, e < g, e < h
fn select_379([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_5([d, e, f, g, h, a, i])
    } else {
        select_12([a, b, c, e, f, g, h, d])
    }
}
/// n = 9, i = 2, b < e, c < d, c < f, f < g, f < h, f < i
fn select_380([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < d {
        select_378([a, b, c, e, f, g, h, i, d])
    } else {
        select_379([b, c, e, d, f, g, h, i, a])
    }
}
/// n = 10, i = 3, a < e, b < f, c < d, c < f, f < g, f < h, f < i, f < j
fn select_381([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_172([d, b, a, f, g, h, i, j, e])
    } else {
        select_335([a, b, c, e, d, f, g, h, i, j])
    }
}
/// n = 10, i = 3, a < e, b < h, b < i, b < j, c < d, c < f, f < g, f < h, f < i, f < j
fn select_382([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < b {
        select_380([d, a, f, g, e, b, h, i, j])
    } else {
        select_381([a, b, c, d, e, f, g, h, i, j])
    }
}
/// n = 13, i = 3, a < e, b < h, b < l, b < m, c < d, c < f, c < h, f < g, f < l, f < m, h < i, h < j, h < k
fn select_383([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if f < h {
        select_382([a, b, c, d, e, f, g, h, l, m])
    } else {
        select_381([a, b, c, d, e, h, f, i, j, k])
    }
}
/// n = 5, i = 3, b < e, c < d
fn select_384([a, b, c, d, e]: [usize; 5]) -> usize {
    if d < e {
        select_44([a, b, d, e])
    } else {
        select_44([a, c, e, d])
    }
}
/// n = 8, i = 4, a < g, b < f, b < g, c < d, c < f, d < e, g < h
fn select_385([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if g < e {
        select_275([a, c, d, f, g, h])
    } else {
        select_384([a, b, d, e, f])
    }
}
/// n = 7, i = 3, a < e, b < e, b < f, b < g, c < d, d < f, d < g
fn select_386([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_11([a, b, f, g])
    } else {
        select_64([b, c, d, e])
    }
}
/// n = 8, i = 3, b < e, b < h, c < d, c < f, c < g, d < h, e < f, e < g
fn select_387([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_242([d, b, a, e, f, g, h])
    } else {
        select_386([a, c, b, e, d, f, g])
    }
}
/// n = 10, i = 4, a < g, a < i, a < j, b < e, b < h, c < d, c < g, c < i, c < j, e < f, e < i, e < j, g < h
fn select_388([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < g {
        select_261([a, c, e, f, d, i, j])
    } else {
        select_387([d, b, a, g, e, i, j, h])
    }
}
/// n = 11, i = 5, a < f, b < d, b < j, b < k, c < e, c < i, d < i, e < g, e < j, e < k, f < h, f < j, f < k
fn select_389([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < f {
        select_385([a, d, c, e, g, i, f, h])
    } else {
        select_388([b, c, f, h, e, g, d, i, j, k])
    }
}
/// n = 14, i = 5, a < e, a < j, b < d, b < j, b < n, c < f, c < i, d < i, e < h, e < n, f < g, f < j, f < n, j < k, j < l, j < m
fn select_390([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if j < e {
        select_381([d, a, f, g, i, j, e, k, l, m])
    } else {
        select_389([a, b, c, d, f, e, g, h, i, j, n])
    }
}
/// n = 16, i = 5, a < e, a < l, a < p, b < d, b < j, b < l, c < f, c < i, d < i, e < h, f < g, f < j, f < l, j < k, j < p, l < m, l < n, l < o
fn select_391([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if j < e {
        select_383([d, a, f, g, i, j, k, l, m, n, o, e, p])
    } else {
        select_390([a, b, c, d, e, f, g, h, i, l, m, n, o, j])
    }
}
/// n = 16, i = 5, a < e, b < l, b < p, c < f, c < j, c < l, d < g, d < i, f < i, g < h, g < j, g < l, j < k, j < p, l < m, l < n, l < o
fn select_392([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_376([a, c, d, e, f, b, g, h, i, j, k, l])
    } else {
        select_391([b, c, d, f, a, g, h, e, i, j, k, l, m, n, o, p])
    }
}
/// n = 16, i = 5, a < f, b < e, b < m, c < g, c < k, c < m, d < h, d < j, g < j, h < i, h < k, h < m, k < l, m < n, m < o, m < p
fn select_393([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < k {
        select_358([a, b, c, d, f, g, e, h, i, j, m, n, o, p, k])
    } else {
        select_392([a, b, c, d, f, g, h, i, j, k, l, m, n, o, p, e])
    }
}
/// n = 18, i = 5, a < f, b < e, c < g, c < k, c < l, d < h, d < j, g < j, h < i, h < k, h < l, k < n, l < m, l < o, l < p, o < r, p < q
fn select_394([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if l < a {
        select_226([b, h, c, i, e, g, j, k, l, m, n, a, o, p, q, r, f])
    } else {
        select_393([b, a, c, d, f, e, g, h, i, j, k, n, l, m, o, p])
    }
}
/// n = 18, i = 5, a < f, b < e, c < g, c < o, d < h, d < l, g < l, h < i, h < j, h < o, j < k, j < m, j < n, m < q, n < p, o < r
fn select_395([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if j < c {
        select_197([a, b, h, i, e, f, j, k, m, n, c, p, q, g, o, r, l])
    } else {
        select_394([a, b, c, d, e, f, g, h, i, l, o, j, k, r, m, n, p, q])
    }
}
/// n = 7, i = 2, b < f, b < g, c < d, c < f, c < g, d < e
fn select_396([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_151([b, d, a, e, f, g])
    } else {
        select_259([a, b, c, f, g, d])
    }
}
/// n = 7, i = 2, b < d, b < g, c < e, c < g, e < f
fn select_397([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < e {
        select_79([a, c, b, d, g, e])
    } else {
        select_242([b, c, d, e, a, f, g])
    }
}
/// n = 9, i = 3, b < e, b < g, c < d, c < g, c < i, d < f, e < i, g < h
fn select_398([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < d {
        select_396([a, e, c, g, h, d, i])
    } else {
        select_397([a, d, b, f, g, h, e])
    }
}
/// n = 9, i = 3, b < e, c < g, c < i, d < f, d < g, f < i, g < h
fn select_399([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if b < c {
        select_106([a, d, b, e, f, c, g])
    } else {
        select_398([a, d, c, b, f, e, g, h, i])
    }
}
/// n = 6, i = 3, a < d, b < e, b < f, c < e, c < f
fn select_400([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < e {
        select_71([b, c, a, d, f])
    } else {
        select_83([a, e, f])
    }
}
/// n = 7, i = 3, a < f, b < d, b < g, c < e, c < f, e < g
fn select_401([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_90([b, e, d, a, f, g])
    } else {
        select_400([b, a, c, d, e, f])
    }
}
/// n = 8, i = 4, a < f, a < h, b < e, b < g, c < d, c < g, g < h
fn select_402([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_401([d, a, b, f, g, e, h])
    } else {
        select_401([e, a, c, f, g, d, h])
    }
}
/// n = 10, i = 4, a < e, b < f, b < h, c < d, c < g, f < j, g < h, g < j, h < i
fn select_403([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < g {
        select_402([b, a, c, d, e, f, g, h])
    } else {
        select_398([d, b, g, a, f, e, h, i, j])
    }
}
/// n = 10, i = 4, a < f, b < e, b < i, c < d, c < g, g < h, g < i, i < j
fn select_404([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < e {
        select_399([d, a, b, g, f, h, i, j, e])
    } else {
        select_403([a, b, c, d, f, e, g, i, j, h])
    }
}
/// n = 7, i = 3, a < g, b < d, b < f, c < e, e < f, e < g
fn select_405([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_90([b, e, d, a, g, f])
    } else {
        select_287([b, a, c, d, e, g])
    }
}
/// n = 6, i = 3, a < f, b < d, c < e, e < f
fn select_406([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if e < d {
        select_92([a, b, e, d, f])
    } else {
        select_44([a, c, d, e])
    }
}
/// n = 7, i = 3, a < e, b < f, c < d, c < g, f < g
fn select_407([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < e {
        select_405([a, c, b, d, f, g, e])
    } else {
        select_406([b, c, a, d, e, f])
    }
}
/// n = 8, i = 4, a < g, a < h, b < e, c < d, c < h, d < f, e < g, e < h
fn select_408([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < d {
        select_90([a, c, g, d, f, h])
    } else {
        select_306([a, f, b, e])
    }
}
/// n = 7, i = 3, a < d, b < f, b < g, c < e, e < f, e < g
fn select_409([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < e {
        select_306([b, d, c, e])
    } else {
        select_27([a, b, f, g, d])
    }
}
/// n = 9, i = 4, a < g, a < h, b < e, b < i, c < d, c < g, d < f, e < h, g < i
fn select_410([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < g {
        select_408([a, b, c, d, e, f, h, g])
    } else {
        select_409([d, b, a, f, g, e, i])
    }
}
/// n = 9, i = 4, a < h, a < i, b < f, b < i, c < d, c < e, d < i, e < g, f < h
fn select_411([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_407([e, d, b, f, g, a, i])
    } else {
        select_410([a, b, c, e, f, g, d, h, i])
    }
}
/// n = 9, i = 4, a < e, a < i, b < d, b < i, c < f, c < g, f < i, g < h
fn select_412([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_411([a, b, c, f, g, d, h, e, i])
    } else {
        select_411([b, a, c, f, g, e, h, d, i])
    }
}
/// n = 12, i = 4, a < g, a < h, b < d, b < h, c < e, c < h, d < g, e < f, h < i, h < j, h < k, h < l
fn select_413([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < d {
        select_335([e, a, b, f, d, h, i, j, k, l])
    } else {
        select_119([d, a, c, g, e, h, i, j, k, l, f])
    }
}
/// n = 12, i = 4, a < e, a < h, b < d, b < h, c < f, c < h, f < g, h < i, h < j, h < k, h < l
fn select_414([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < e {
        select_413([a, b, c, d, f, g, e, h, i, j, k, l])
    } else {
        select_413([b, a, c, e, f, g, d, h, i, j, k, l])
    }
}
/// n = 12, i = 4, a < f, a < i, b < e, b < i, c < d, c < g, c < i, g < h, i < j, i < k, i < l
fn select_415([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < i {
        select_412([a, b, c, e, f, d, g, h, i])
    } else {
        select_414([a, b, c, e, f, g, h, i, d, j, k, l])
    }
}
/// n = 14, i = 4, a < f, a < j, b < e, b < i, b < j, c < d, c < g, c < j, g < h, g < i, i < k, j < l, j < m, j < n
fn select_416([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < j {
        select_404([a, b, c, d, e, f, g, h, i, k])
    } else {
        select_415([a, b, c, d, e, f, g, h, j, l, m, n])
    }
}
/// n = 8, i = 3, a < d, b < f, b < g, b < h, c < e, c < f, e < g, e < h
fn select_417([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_66([b, c, a, d, e, f])
    } else {
        select_150([b, e, f, a, d, g, h])
    }
}
/// n = 7, i = 2, a < c, b < d, d < e, d < f, d < g
fn select_418([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_4([a, e, f, g])
    } else {
        select_10([c, b, d])
    }
}
/// n = 9, i = 3, a < d, a < e, b < e, b < f, c < d, c < f, f < g, f < h, f < i
fn select_419([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_4([a, g, h, i])
    } else {
        select_19([b, c, d, e, f])
    }
}
/// n = 9, i = 3, a < e, b < e, b < f, c < d, c < f, f < g, f < h, f < i
fn select_420([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_418([d, b, a, f, g, h, i])
    } else {
        select_419([a, b, c, d, e, f, g, h, i])
    }
}
/// n = 12, i = 3, a < e, a < f, b < d, b < g, c < f, c < g, c < k, c < l, e < k, e < l, g < h, g < i, g < j
fn select_421([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < g {
        select_417([b, c, a, d, e, f, k, l])
    } else {
        select_420([a, c, b, d, f, g, h, i, j])
    }
}
/// n = 9, i = 2, a < c, a < i, b < d, b < e, b < i, d < h, e < f, e < g
fn select_422([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_24([d, e, a, f, g, h])
    } else {
        select_150([a, b, c, d, h, e, i])
    }
}
/// n = 7, i = 2, a < e, a < g, b < c, b < d, b < g, e < f
fn select_423([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < e {
        select_73([c, d, a, g])
    } else {
        select_90([b, a, d, e, f, g])
    }
}
/// n = 9, i = 2, a < h, a < i, b < d, b < g, c < e, c < g, c < h, c < i, e < f
fn select_424([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if b < a {
        select_423([c, b, a, d, e, f, g])
    } else {
        select_86([a, c, e, b, f, d, h, i])
    }
}
/// n = 10, i = 2, a < j, b < d, b < i, c < e, c < f, c < i, c < j, e < h, f < g
fn select_425([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_422([b, c, d, f, e, a, h, g, i])
    } else {
        select_424([a, b, c, d, f, g, i, e, j])
    }
}
/// n = 7, i = 2, a < f, a < g, b < d, b < e, b < g, c < d, c < e, c < f
fn select_426([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_72([b, c, f, g])
    } else {
        select_27([a, c, d, e, g])
    }
}
/// n = 7, i = 2, a < g, b < e, b < f, b < g, c < d, c < e, c < f
fn select_427([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_27([d, b, e, f, a])
    } else {
        select_426([a, b, c, e, f, d, g])
    }
}
/// n = 10, i = 2, b < d, b < i, b < j, c < e, c < i, c < j, e < f, e < g, e < h
fn select_428([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < e {
        select_427([a, c, b, d, i, j, e])
    } else {
        select_30([b, c, d, e, a, f, g, h, i, j])
    }
}
/// n = 14, i = 3, a < d, a < h, b < e, b < f, b < g, c < f, c < g, c < h, c < k, e < k, f < j, g < i, h < l, h < m, h < n
fn select_429([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if b < a {
        select_425([e, a, c, d, f, g, i, j, h, k])
    } else {
        select_428([d, b, c, e, h, l, m, n, f, g])
    }
}
/// n = 14, i = 3, a < f, b < g, b < h, c < e, c < i, d < f, d < g, d < h, d < i, g < n, h < m, i < j, i < k, i < l
fn select_430([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if a < b {
        select_421([a, c, d, e, b, f, i, j, k, l, g, h])
    } else {
        select_429([c, b, d, e, a, g, h, i, m, n, f, j, k, l])
    }
}
/// n = 9, i = 3, a < d, a < i, b < e, b < f, b < i, c < e, c < f, c < i, f < g, f < h
fn select_431([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < d {
        select_316([e, a, f, g, h, i])
    } else {
        select_45([b, c, a, d, e, i])
    }
}
/// n = 12, i = 3, a < e, a < f, b < d, b < g, c < e, c < f, c < g, f < k, f < l, g < h, g < i, g < j
fn select_432([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < a {
        select_49([d, g, a, h, i, j])
    } else {
        select_431([b, a, c, d, e, f, k, l, g])
    }
}
/// n = 10, i = 2, a < c, a < j, b < d, b < e, b < f, b < j, d < i, e < h, f < g
fn select_433([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < f {
        select_422([a, b, c, e, d, f, i, h, j])
    } else {
        select_422([a, b, c, e, f, d, g, h, j])
    }
}
/// n = 7, i = 2, a < g, b < d, b < e, b < f, c < d, c < e, c < f, c < g
fn select_434([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_10([b, c, g])
    } else {
        select_18([a, c, d, e, f])
    }
}
/// n = 10, i = 2, b < h, b < i, b < j, c < d, c < h, c < i, c < j, d < e, d < f, d < g
fn select_435([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_214([b, d, a, e, f, g, h, i, j])
    } else {
        select_434([a, b, c, h, i, j, d])
    }
}
/// n = 14, i = 3, a < d, a < h, b < e, b < f, b < g, c < e, c < f, c < g, c < h, e < k, f < j, g < i, h < l, h < m, h < n
fn select_436([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if b < a {
        select_433([a, c, d, e, f, g, i, j, k, h])
    } else {
        select_435([d, b, c, h, l, m, n, e, f, g])
    }
}
/// n = 15, i = 4, a < d, a < j, b < f, b < g, b < j, c < e, c < h, c < i, c < j, e < g, f < h, f < i, h < l, i < k, j < m, j < n, j < o
fn select_437([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if e < f {
        select_432([e, a, b, d, g, f, j, m, n, o, h, i])
    } else {
        select_436([a, f, c, d, e, h, i, j, k, l, g, m, n, o])
    }
}
/// n = 15, i = 4, a < f, a < j, b < e, b < h, b < i, b < j, c < d, c < g, c < j, g < h, g < i, h < l, i < k, j < m, j < n, j < o
fn select_438([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if d < e {
        select_430([d, g, a, b, f, e, h, i, j, m, n, o, k, l])
    } else {
        select_437([a, c, b, f, e, g, d, h, i, j, k, l, m, n, o])
    }
}
/// n = 15, i = 4, a < f, a < k, b < e, b < h, b < k, c < d, c < g, c < j, c < k, g < i, h < j, j < l, k < m, k < n, k < o
fn select_439([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < h {
        select_416([a, b, c, d, e, f, g, i, h, k, j, m, n, o])
    } else {
        select_438([a, c, b, e, d, f, h, g, j, k, l, i, m, n, o])
    }
}
/// n = 9, i = 3, a < c, a < d, b < e, b < i, d < i, e < f, e < g, g < h
fn select_440([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < d {
        select_62([a, e, f, c, g, h])
    } else {
        select_268([b, a, c, d, e, f, i])
    }
}
/// n = 10, i = 3, a < c, a < d, a < i, b < e, b < j, d < j, e < f, e < g, e < i, g < h
fn select_441([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < d {
        select_39([a, e, f, c, g, h, i])
    } else {
        select_53([b, a, c, d, e, f, i, j])
    }
}
/// n = 10, i = 3, a < c, a < e, a < i, b < d, b < f, b < j, d < h, e < j, f < g, f < i
fn select_442([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < f {
        select_440([a, b, c, e, d, h, f, g, j])
    } else {
        select_441([a, b, c, e, f, g, d, h, i, j])
    }
}
/// n = 9, i = 3, a < f, a < g, b < d, b < e, c < f, c < g, c < h, e < h, g < i
fn select_443([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_102([d, c, e, a, h])
    } else {
        select_67([b, c, a, d, f, e, g, i])
    }
}
/// n = 10, i = 3, a < h, b < d, b < e, b < i, c < f, c < h, c < j, e < j, f < g, f < i
fn select_444([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < f {
        select_443([a, b, c, d, e, h, f, j, g])
    } else {
        select_441([b, c, d, e, f, g, a, h, i, j])
    }
}
/// n = 10, i = 3, b < e, b < f, b < i, c < d, c < g, c < j, f < j, g < h, g < i
fn select_445([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_442([b, c, e, d, f, g, h, a, i, j])
    } else {
        select_444([a, b, c, e, f, g, h, d, i, j])
    }
}
/// n = 7, i = 3, a < d, b < e, c < e, e < f, e < g
fn select_446([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_3([a, f, g])
    } else {
        select_44([d, b, c, e])
    }
}
/// n = 7, i = 4, a < e, b < f, c < f, d < e, d < g, f < g
fn select_447([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < e {
        select_44([a, d, f, g])
    } else {
        select_70([b, c, e])
    }
}
/// n = 8, i = 4, a < f, b < f, b < g, c < e, c < g, d < e, d < g, g < h
fn select_448([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if g < e {
        select_446([a, c, d, f, g, e, h])
    } else {
        select_447([a, c, d, b, f, e, g])
    }
}
/// n = 10, i = 4, a < f, b < e, b < i, b < j, c < f, c < g, d < e, d < g, g < h, g < i, g < j
fn select_449([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_153([b, g, h, e, a, f, i, j])
    } else {
        select_448([b, d, a, c, f, e, g, h])
    }
}
/// n = 8, i = 4, a < g, a < h, b < e, b < h, c < f, c < h, d < f, d < h, f < g
fn select_450([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < e {
        select_78([a, b, f, e, g, h])
    } else {
        select_347([a, e, c, d, f, h])
    }
}
/// n = 7, i = 4, a < g, b < f, c < e, c < g, d < e, d < f
fn select_451([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < g {
        select_384([a, b, c, e, f])
    } else {
        select_384([b, a, d, e, g])
    }
}
/// n = 9, i = 5, a < h, a < i, b < g, b < i, c < f, c < i, d < e, d < g, e < i, f < h
fn select_452([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < f {
        select_450([a, b, c, e, g, f, h, i])
    } else {
        select_451([a, b, f, d, e, g, h])
    }
}
/// n = 11, i = 5, a < e, a < g, a < k, b < h, b < i, c < g, c < i, d < f, d < i, f < h, i < j, i < k
fn select_453([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if i < e {
        select_449([f, a, b, c, g, h, i, j, e, k])
    } else {
        select_452([b, c, d, a, e, f, g, h, i])
    }
}
/// n = 11, i = 5, a < g, a < h, a < k, b < h, b < i, c < f, c < i, d < e, d < i, i < j, i < k
fn select_454([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_453([a, c, b, d, g, e, h, f, i, j, k])
    } else {
        select_453([a, d, b, c, g, f, h, e, i, j, k])
    }
}
/// n = 12, i = 5, a < f, a < l, b < g, b < h, b < l, c < h, c < i, d < e, d < i, g < k, i < j, i < k, i < l
fn select_455([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if i < a {
        select_445([e, b, i, j, h, g, a, f, l, k])
    } else {
        select_454([b, c, a, d, e, f, g, h, i, j, l])
    }
}
/// n = 16, i = 5, a < f, b < e, b < l, c < g, c < j, c < l, d < h, d < j, g < k, h < i, h < k, h < l, k < m, l < n, l < o, l < p
fn select_456([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if h < a {
        select_439([b, c, h, i, j, e, a, g, f, k, l, m, n, o, p])
    } else {
        select_455([b, c, d, a, f, e, g, j, h, i, k, l])
    }
}
/// n = 18, i = 5, a < f, b < e, c < g, c < j, c < k, d < h, d < j, g < o, h < i, h < k, h < o, k < l, k < m, k < n, m < q, n < p, o < r
fn select_457([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if k < b {
        select_187([a, h, c, j, i, f, g, k, l, b, m, n, o, p, q, e, r])
    } else {
        select_456([a, b, c, d, e, f, g, h, i, j, o, k, r, l, m, n])
    }
}
/// n = 18, i = 5, a < f, b < e, c < g, c < j, d < h, d < j, g < q, h < i, h < k, h < q, k < l, k < m, k < n, m < p, n < o, q < r
fn select_458([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if k < c {
        select_61([a, b, h, i, e, f, k, l, m, n, c, j, o, p, g, q])
    } else {
        select_457([a, b, c, d, e, f, g, h, i, j, k, l, m, n, q, o, p, r])
    }
}
/// n = 18, i = 5, a < j, b < g, c < f, d < o, e < h, e < j, h < i, h < k, h < o, k < l, k < m, k < n, m < q, n < p, o < r
fn select_459([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if d < a {
        select_395([b, c, d, e, f, g, a, h, i, k, l, j, m, n, o, p, q, r])
    } else {
        select_458([b, c, a, e, f, g, d, h, i, j, k, l, m, n, p, q, o, r])
    }
}
/// n = 18, i = 5, b < h, c < g, d < o, e < f, e < i, i < j, i < k, i < o, k < l, k < m, k < n, m < q, n < p, o < r
fn select_460([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if f < a {
        select_327([b, c, d, e, g, h, f, i, j, a, k, l, m, n, o, p, q, r])
    } else {
        select_459([a, b, c, d, e, g, h, i, j, f, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, d < h, e < o, f < g, f < i, i < j, i < k, i < o, k < l, k < m, k < n, m < q, n < p, o < r
fn select_461([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_460([c, a, d, e, f, g, h, b, i, j, k, l, m, n, o, p, q, r])
    } else {
        select_460([c, b, d, e, f, g, h, a, i, j, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, f < o, g < h, g < i, i < j, i < k, i < o, k < l, k < m, k < n, m < q, n < p, o < r
fn select_462([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_461([c, d, e, a, f, g, h, b, i, j, k, l, m, n, o, p, q, r])
    } else {
        select_461([c, d, e, b, f, g, h, a, i, j, k, l, m, n, o, p, q, r])
    }
}
/// n = 10, i = 1, c < j, d < i, e < f, e < g, e < h
fn select_463([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_8([a, b, c, e, f, g, h, d, j])
    } else {
        select_8([a, b, d, e, f, g, h, c, i])
    }
}
/// n = 9, i = 1, a < i, b < h, c < d, c < e, c < f, c < g
fn select_464([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_155([a, c, d, e, f, g, b, i])
    } else {
        select_155([b, c, d, e, f, g, a, h])
    }
}
/// n = 9, i = 1, c < i, d < e, d < f, d < g, d < h
fn select_465([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_464([a, c, d, e, f, g, h, i, b])
    } else {
        select_464([b, c, d, e, f, g, h, i, a])
    }
}
/// n = 12, i = 2, b < e, b < h, b < l, c < d, c < f, c < g, c < l, f < j, g < i, h < k
fn select_466([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if b < c {
        select_465([a, e, h, c, d, f, g, l, k])
    } else {
        select_463([a, d, f, g, b, e, h, l, i, j])
    }
}
/// n = 14, i = 2, b < e, b < h, c < d, c < f, c < g, c < i, f < m, g < l, h < n, i < j, i < k
fn select_467([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < b {
        select_463([a, d, f, g, i, b, j, k, l, m])
    } else {
        select_466([a, b, c, d, e, f, g, h, l, m, n, i])
    }
}
/// n = 14, i = 2, b < g, c < f, d < e, d < h, d < i, d < j, h < n, i < m, j < k, j < l
fn select_468([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if b < c {
        select_467([a, b, d, e, g, h, i, c, j, k, l, m, n, f])
    } else {
        select_467([a, c, d, e, f, h, i, b, j, k, l, m, n, g])
    }
}
/// n = 14, i = 2, d < g, e < f, e < h, e < i, e < j, h < n, i < m, j < k, j < l
fn select_469([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if a < b {
        select_468([c, a, d, e, f, g, b, h, i, j, k, l, m, n])
    } else {
        select_468([c, b, d, e, f, g, a, h, i, j, k, l, m, n])
    }
}
/// n = 9, i = 2, a < d, b < c, b < e, e < f, e < g, e < h, e < i
fn select_470([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < a {
        select_23([c, e, f, g, h, i, a])
    } else {
        select_227([a, b, d, e, f, g, h, i, c])
    }
}
/// n = 9, i = 2, c < d, c < e, e < f, e < g, e < h, e < i
fn select_471([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_470([a, c, d, b, e, f, g, h, i])
    } else {
        select_470([b, c, d, a, e, f, g, h, i])
    }
}
/// n = 9, i = 3, a < g, a < i, b < e, b < i, c < d, c < g, c < i, e < f, g < h
fn select_472([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_286([d, b, a, g, h, i, e])
    } else {
        select_231([a, c, b, e, f, g, d, h, i])
    }
}
/// n = 10, i = 3, a < e, a < f, a < j, b < d, b < f, b < j, c < d, c < e, c < j, d < g, e < h, f < i
fn select_473([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_137([a, c, d, f, g, i, j])
    } else {
        select_137([b, c, e, f, h, i, j])
    }
}
/// n = 10, i = 3, a < g, a < j, b < f, b < g, b < j, c < d, c < f, c < j, d < e, f < h, g < i
fn select_474([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_85([b, d, a, e, f, h])
    } else {
        select_473([a, b, c, f, d, g, h, e, i, j])
    }
}
/// n = 11, i = 3, a < d, a < h, a < k, b < g, b < h, b < k, c < e, c < g, c < k, e < f, g < i, h < j
fn select_475([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < g {
        select_472([b, c, a, d, e, f, h, j, k])
    } else {
        select_474([a, b, c, e, f, g, h, i, j, k])
    }
}
/// n = 11, i = 3, a < f, a < h, a < k, b < g, b < h, b < k, c < d, c < e, c < g, c < k, g < i, h < j
fn select_476([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_475([a, b, c, f, d, e, g, h, i, j, k])
    } else {
        select_475([a, b, c, f, e, d, g, h, i, j, k])
    }
}
/// n = 14, i = 3, a < g, a < h, b < f, b < h, b < i, c < d, c < e, c < g, c < i, g < m, h < n, i < j, i < k, i < l
fn select_477([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < a {
        select_471([d, e, b, f, i, a, j, k, l])
    } else {
        select_476([b, a, c, d, e, f, g, h, m, n, i])
    }
}
/// n = 10, i = 4, a < e, a < i, b < c, b < d, d < f, d < i, d < j, e < g, e < h, e < j
fn select_478([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_34([c, f, a, i, e, g, h, j])
    } else {
        select_34([g, h, b, c, d, f, i, j])
    }
}
/// n = 13, i = 4, a < e, a < i, b < c, b < d, b < j, d < f, d < i, e < g, e < h, e < j, j < k, j < l, j < m
fn select_479([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if j < d {
        select_471([g, h, b, c, j, d, k, l, m])
    } else {
        select_478([a, b, c, d, e, f, g, h, i, j])
    }
}
/// n = 15, i = 4, a < c, a < d, a < k, b < e, b < f, d < i, e < j, f < g, f < h, f < j, f < k, j < l, k < m, k < n, k < o
fn select_480([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if e < d {
        select_477([e, a, f, g, h, c, j, d, k, m, n, o, l, i])
    } else {
        select_479([b, a, c, d, f, i, g, h, e, k, m, n, o])
    }
}
/// n = 8, i = 2, a < d, a < e, b < c, b < f, f < g, f < h
fn select_481([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < a {
        select_18([c, f, a, g, h])
    } else {
        select_176([b, a, d, e, c, f])
    }
}
/// n = 7, i = 2, a < e, a < f, a < g, b < c, b < d, b < f, b < g
fn select_482([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < d {
        select_150([a, b, e, c, d, f, g])
    } else {
        select_150([a, b, e, d, c, f, g])
    }
}
/// n = 9, i = 2, a < d, a < e, a < i, b < c, b < f, b < i, f < g, f < h
fn select_483([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_18([c, f, a, g, h])
    } else {
        select_482([b, a, d, e, c, f, i])
    }
}
/// n = 9, i = 2, a < g, a < i, b < f, b < h, b < i, c < d, c < e, c < h
fn select_484([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_481([c, a, g, d, e, b, f, i])
    } else {
        select_483([c, b, f, d, e, a, g, i, h])
    }
}
/// n = 10, i = 4, a < e, b < c, b < d, b < i, d < f, d < j, e < g, e < j, g < h, g < i
fn select_485([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < g {
        select_405([c, d, a, f, e, j, g])
    } else {
        select_245([e, b, d, g, h, f, c, i, j])
    }
}
/// n = 12, i = 4, a < c, a < d, a < l, b < e, d < f, e < g, e < h, g < k, g < l, h < i, h < j
fn select_486([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < d {
        select_484([g, a, h, i, j, c, k, d, l])
    } else {
        select_485([b, a, c, d, e, f, g, k, l, h])
    }
}
/// n = 7, i = 1, b < c, b < d, b < e, b < f, b < g
fn select_487([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < a {
        select_22([c, d, e, f, g])
    } else {
        select_49([a, b, d, e, f, g])
    }
}
/// n = 10, i = 2, a < d, a < e, b < c, b < f, f < g, f < h, f < i, f < j
fn select_488([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < a {
        select_23([c, f, g, h, i, j, a])
    } else {
        select_174([a, b, d, e, f, g, h, i, j, c])
    }
}
/// n = 11, i = 2, a < d, a < e, b < c, b < f, f < g, f < h, f < i, f < j, f < k
fn select_489([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_487([c, f, g, h, i, j, k])
    } else {
        select_488([a, b, c, d, e, f, h, i, j, k])
    }
}
/// n = 7, i = 3, b < e, c < d, c < f, c < g, e < f, e < g
fn select_490([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_38([c, e, a, d, f, g])
    } else {
        select_71([a, b, c, d, e])
    }
}
/// n = 10, i = 4, a < c, a < d, b < e, d < f, d < j, e < g, e < j, g < h, g < i
fn select_491([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < d {
        select_176([a, g, h, i, c, d])
    } else {
        select_490([c, b, d, f, e, g, j])
    }
}
/// n = 14, i = 4, a < c, a < d, a < j, b < e, d < f, e < g, e < j, g < h, g < i, j < k, j < l, j < m, j < n
fn select_492([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if j < d {
        select_489([g, a, c, h, i, j, d, k, l, m, n])
    } else {
        select_491([a, b, c, d, e, f, g, h, i, j])
    }
}
/// n = 15, i = 4, a < c, a < d, a < l, b < e, d < f, e < g, e < h, e < l, g < k, h < i, h < j, l < m, l < n, l < o
fn select_493([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < l {
        select_486([a, b, c, d, e, f, g, h, i, j, k, l])
    } else {
        select_492([a, b, c, d, e, f, h, i, j, l, g, m, n, o])
    }
}
/// n = 15, i = 4, a < c, a < d, a < l, b < e, d < h, e < f, e < g, e < i, e < l, i < j, i < k, l < m, l < n, l < o
fn select_494([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if f < g {
        select_493([a, b, c, d, e, h, f, i, j, k, g, l, m, n, o])
    } else {
        select_493([a, b, c, d, e, h, g, i, j, k, f, l, m, n, o])
    }
}
/// n = 15, i = 4, a < d, a < e, a < l, b < c, b < f, e < i, f < g, f < h, f < j, f < l, j < k, l < m, l < n, l < o
fn select_495([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if c < j {
        select_480([a, b, d, e, c, f, g, h, i, j, l, k, m, n, o])
    } else {
        select_494([a, b, d, e, f, g, h, i, j, c, k, l, m, n, o])
    }
}
/// n = 17, i = 4, a < d, a < e, b < c, b < f, e < i, f < g, f < h, f < j, f < k, j < m, k < l, k < n, k < o, n < q, o < p
fn select_496([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if k < a {
        select_469([c, g, h, j, k, l, m, n, o, a, d, e, p, q])
    } else {
        select_495([a, b, c, d, e, f, g, h, i, j, m, k, l, n, o])
    }
}
/// n = 10, i = 1, b < j, c < h, c < i, d < e, d < f, d < g
fn select_497([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_7([a, c, d, e, f, g, h, i, b])
    } else {
        select_198([b, c, d, e, f, g, h, i, a, j])
    }
}
/// n = 10, i = 1, d < i, d < j, e < f, e < g, e < h
fn select_498([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_497([c, a, d, e, f, g, h, i, j, b])
    } else {
        select_497([c, b, d, e, f, g, h, i, j, a])
    }
}
/// n = 10, i = 2, b < j, c < d, c < e, c < j, d < i, e < f, e < g, e < h
fn select_499([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_7([b, d, e, f, g, h, a, i, j])
    } else {
        select_13([a, b, c, e, f, g, h, j, d])
    }
}
/// n = 10, i = 2, b < j, c < d, c < e, c < f, c < j, f < g, f < h, f < i
fn select_500([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_499([a, b, c, d, f, g, h, i, e, j])
    } else {
        select_499([a, b, c, e, f, g, h, i, d, j])
    }
}
/// n = 11, i = 2, c < d, c < e, c < f, c < g, f < k, g < h, g < i, g < j
fn select_501([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_498([b, d, e, f, g, h, i, j, a, k])
    } else {
        select_500([b, a, c, d, e, g, h, i, j, f])
    }
}
/// n = 10, i = 1, a < j, b < h, b < i, c < d, c < e, c < f, c < g
fn select_502([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_155([a, c, d, e, f, g, b, j])
    } else {
        select_214([b, c, d, e, f, g, a, h, i])
    }
}
/// n = 10, i = 1, c < i, c < j, d < e, d < f, d < g, d < h
fn select_503([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_502([a, c, d, e, f, g, h, i, j, b])
    } else {
        select_502([b, c, d, e, f, g, h, i, j, a])
    }
}
/// n = 10, i = 2, a < j, b < i, c < d, c < i, c < j, d < e, d < f, d < g, d < h
fn select_504([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_227([a, c, b, d, e, f, g, h, j])
    } else {
        select_227([b, c, a, d, e, f, g, h, i])
    }
}
/// n = 10, i = 2, b < j, c < d, c < e, c < j, e < f, e < g, e < h, e < i
fn select_505([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_464([b, d, e, f, g, h, i, a, j])
    } else {
        select_504([a, b, c, e, f, g, h, i, j, d])
    }
}
/// n = 11, i = 2, c < d, c < e, c < f, e < k, f < g, f < h, f < i, f < j
fn select_506([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_503([b, d, e, f, g, h, i, j, a, k])
    } else {
        select_505([b, a, c, d, f, g, h, i, j, e])
    }
}
/// n = 12, i = 2, c < g, c < i, c < l, d < e, d < f, d < h, d < l, h < j, i < k
fn select_507([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if c < d {
        select_506([a, b, c, g, i, d, e, f, h, l, k])
    } else {
        select_501([a, b, d, e, f, h, c, g, i, l, j])
    }
}
/// n = 14, i = 2, c < g, c < i, d < e, d < f, d < h, d < j, h < m, i < n, j < k, j < l
fn select_508([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if j < c {
        select_501([a, b, d, e, f, h, j, c, k, l, m])
    } else {
        select_507([a, b, c, d, e, f, g, h, i, m, n, j])
    }
}
/// n = 14, i = 2, c < i, d < h, e < f, e < g, e < j, e < k, j < n, k < l, k < m
fn select_509([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if c < d {
        select_508([a, b, c, e, f, g, i, j, d, k, l, m, n, h])
    } else {
        select_508([a, b, d, e, f, g, h, j, c, k, l, m, n, i])
    }
}
/// n = 8, i = 3, a < d, b < f, b < h, c < e, c < f, e < h, f < g
fn select_510([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < d {
        select_256([a, e, b, f, g, h])
    } else {
        select_406([b, a, c, d, e, h])
    }
}
/// n = 9, i = 3, a < d, b < e, b < f, c < e, c < f, e < i, f < g, f < h
fn select_511([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_24([e, f, a, g, h, i])
    } else {
        select_248([a, b, c, d, e, i, f])
    }
}
/// n = 9, i = 3, a < e, b < f, b < g, c < d, c < f, c < g, f < i, g < h
fn select_512([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < f {
        select_510([a, b, c, e, d, g, h, f])
    } else {
        select_511([a, b, c, e, g, f, d, i, h])
    }
}
/// n = 10, i = 3, a < h, b < e, b < i, c < d, c < f, c < h, f < g, f < i, h < j
fn select_513([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_82([d, b, f, g, e, a, h, i])
    } else {
        select_512([b, a, c, d, e, f, h, j, g])
    }
}
/// n = 7, i = 2, a < e, a < f, a < g, b < c, b < d, b < g
fn select_514([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < e {
        select_176([a, b, c, d, f, g])
    } else {
        select_176([b, a, e, f, d, g])
    }
}
/// n = 8, i = 3, b < d, b < g, b < h, c < e, c < g, e < f, e < h
fn select_515([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_514([b, e, a, f, d, g, h])
    } else {
        select_307([a, b, c, d, g, e, f])
    }
}
/// n = 9, i = 3, a < f, a < i, b < e, b < f, c < d, c < e, d < i, e < g, f < h
fn select_516([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < d {
        select_310([a, c, f, e, d, g, h])
    } else {
        select_132([a, b, c, d, f, h, e, i])
    }
}
/// n = 9, i = 3, a < e, a < g, b < d, b < f, c < f, c < g, f < h, g < i
fn select_517([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_516([a, c, b, d, f, g, h, i, e])
    } else {
        select_516([b, c, a, e, g, f, i, h, d])
    }
}
/// n = 11, i = 4, a < c, a < e, b < d, b < f, d < i, e < h, e < k, f < g, f < i, f < k, i < j
fn select_518([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < d {
        select_515([c, e, b, h, f, g, d, k])
    } else {
        select_517([a, f, d, g, c, i, e, j, h])
    }
}
/// n = 12, i = 4, a < c, a < d, b < e, b < f, d < h, e < k, f < g, f < i, f < k, i < j, k < l
fn select_519([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if i < d {
        select_513([e, a, f, g, c, i, j, k, d, l])
    } else {
        select_518([a, b, c, e, d, f, g, h, k, l, i])
    }
}
/// n = 11, i = 2, a < c, a < d, a < k, b < e, b < k, d < j, e < f, e < g, e < h, e < i
fn select_520([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_22([a, f, g, h, i])
    } else {
        select_316([c, d, b, e, k, j])
    }
}
/// n = 11, i = 2, a < d, a < e, b < c, b < f, e < k, f < g, f < h, f < i, f < j
fn select_521([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < a {
        select_23([c, f, g, h, i, j, a])
    } else {
        select_520([a, b, d, e, f, g, h, i, j, k, c])
    }
}
/// n = 11, i = 2, a < f, b < e, c < d, c < g, g < h, g < i, g < j, g < k
fn select_522([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_521([a, c, d, f, b, g, h, i, j, k, e])
    } else {
        select_521([b, c, d, e, a, g, h, i, j, k, f])
    }
}
/// n = 10, i = 2, a < c, a < d, b < e, d < j, e < f, e < g, e < h, e < i
fn select_523([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_22([a, f, g, h, i])
    } else {
        select_42([c, b, d, j, e])
    }
}
/// n = 11, i = 2, a < e, b < d, b < k, c < f, c < k, f < g, f < h, f < i, f < j
fn select_524([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_523([a, c, e, b, f, g, h, i, j, d])
    } else {
        select_520([b, c, d, a, f, g, h, i, j, e, k])
    }
}
/// n = 11, i = 3, a < e, b < e, b < f, b < k, c < d, c < f, d < k, f < g, f < h, f < i, f < j
fn select_525([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_227([d, b, a, f, g, h, i, j, k])
    } else {
        select_129([a, b, c, d, e, f, g, h, i, j])
    }
}
/// n = 12, i = 3, a < g, b < d, b < h, c < e, c < g, c < h, e < f, h < i, h < j, h < k, h < l
fn select_526([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < d {
        select_524([a, e, b, f, g, h, i, j, k, l, d])
    } else {
        select_525([a, c, b, d, g, h, i, j, k, l, e])
    }
}
/// n = 12, i = 3, b < e, b < h, c < d, c < f, c < h, f < g, h < i, h < j, h < k, h < l
fn select_527([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < a {
        select_522([d, f, b, e, g, a, h, i, j, k, l])
    } else {
        select_526([a, b, c, e, f, g, d, h, i, j, k, l])
    }
}
/// n = 6, i = 2, a < f, b < e, c < d, c < f
fn select_528([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if b < a {
        select_107([c, b, a, e, d])
    } else {
        select_90([c, a, d, b, e, f])
    }
}
/// n = 7, i = 2, a < f, a < g, b < e, b < g, c < d, c < f
fn select_529([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if b < c {
        select_42([e, a, c, d, g])
    } else {
        select_42([d, a, b, e, f])
    }
}
/// n = 7, i = 2, b < g, c < f, c < g, d < e, d < f
fn select_530([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_528([c, a, d, e, b, f])
    } else {
        select_529([c, b, d, e, a, f, g])
    }
}
/// n = 9, i = 3, a < f, b < f, b < g, b < h, c < d, d < e, d < g, d < h, f < i
fn select_531([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_173([a, e, b, g, h])
    } else {
        select_300([b, c, d, f, e, i])
    }
}
/// n = 10, i = 3, a < d, a < j, b < c, b < h, b < i, c < e, c < f, c < j, d < g, d < h, d < i
fn select_532([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < c {
        select_18([g, b, c, h, i])
    } else {
        select_173([e, f, a, d, j])
    }
}
/// n = 10, i = 3, b < e, b < j, c < d, c < h, c < i, d < g, d < j, e < f, e < h, e < i
fn select_533([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < d {
        select_531([a, c, b, e, f, d, h, i, g])
    } else {
        select_532([b, c, d, e, a, g, f, h, i, j])
    }
}
/// n = 10, i = 3, b < f, b < j, c < d, c < e, c < i, e < g, e < j, f < h, f < i
fn select_534([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < f {
        select_530([a, d, b, e, g, j, f])
    } else {
        select_533([a, b, c, e, f, h, g, d, i, j])
    }
}
/// n = 10, i = 4, a < d, a < e, b < c, b < f, d < j, e < h, e < i, f < g, f < i, f < j
fn select_535([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_75([c, f, a, g, e, h, d, i])
    } else {
        select_54([d, e, b, h, f, g, c, i, j])
    }
}
/// n = 11, i = 4, a < d, a < e, b < c, b < f, e < h, e < k, f < g, f < i, f < k, i < j
fn select_536([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if i < d {
        select_534([c, a, f, g, i, e, j, h, k, d])
    } else {
        select_535([a, b, c, d, e, f, g, h, k, i])
    }
}
/// n = 14, i = 4, a < d, a < e, a < k, b < c, b < f, e < h, f < g, f < i, f < k, i < j, k < l, k < m, k < n
fn select_537([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if k < e {
        select_527([c, a, f, g, d, i, j, k, e, l, m, n])
    } else {
        select_536([a, b, c, d, e, f, g, h, i, j, k])
    }
}
/// n = 16, i = 4, a < c, a < d, a < l, b < e, b < f, d < h, e < k, f < g, f < i, f < k, f < l, i < j, k < m, l < n, l < o, l < p
fn select_538([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if k < l {
        select_519([a, b, c, d, e, f, g, h, i, j, k, m])
    } else {
        select_537([a, b, e, c, d, f, g, h, i, j, l, n, o, p])
    }
}
/// n = 9, i = 2, a < i, b < d, b < h, c < e, c < h, c < i, e < f, e < g
fn select_539([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < e {
        select_243([a, b, c, d, h, e, i])
    } else {
        select_12([b, c, d, e, a, f, g, h])
    }
}
/// n = 9, i = 2, b < e, b < i, c < d, c < f, c < i, f < g, f < h
fn select_540([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_422([b, c, e, d, f, g, h, a, i])
    } else {
        select_539([a, b, c, e, f, g, h, i, d])
    }
}
/// n = 7, i = 1, c < d, c < e, c < f, c < g
fn select_541([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_23([a, c, d, e, f, g, b])
    } else {
        select_23([b, c, d, e, f, g, a])
    }
}
/// n = 7, i = 2, b < e, b < f, b < g, c < d, c < f, c < g
fn select_542([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < e {
        select_260([a, b, c, d, f, g])
    } else {
        select_260([a, c, b, e, f, g])
    }
}
/// n = 10, i = 2, b < e, b < j, c < d, c < f, c < j, f < g, f < h, f < i
fn select_543([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < b {
        select_541([a, d, f, b, g, h, i])
    } else {
        select_542([a, b, c, d, e, f, j])
    }
}
/// n = 13, i = 2, b < e, b < f, b < m, c < d, c < g, c < m, f < k, f < l, g < h, g < i, g < j
fn select_544([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if f < g {
        select_540([a, c, b, e, d, f, k, l, m])
    } else {
        select_543([a, b, c, d, e, g, h, i, j, m])
    }
}
/// n = 8, i = 3, b < d, b < g, b < h, c < e, e < f, e < g, e < h
fn select_545([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < d {
        select_260([a, b, e, f, g, h])
    } else {
        select_490([a, c, b, d, e, g, h])
    }
}
/// n = 11, i = 3, b < d, b < k, c < e, e < f, e < g, e < k, g < h, g < i, g < j
fn select_546([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < b {
        select_541([a, f, g, b, h, i, j])
    } else {
        select_545([a, b, c, d, e, f, g, k])
    }
}
/// n = 16, i = 4, a < c, a < d, a < k, b < e, d < g, e < f, e < h, e < k, h < i, h < j, j < l, j < m, k < n, k < o, k < p
fn select_547([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if h < d {
        select_544([f, h, a, c, i, j, k, n, o, p, l, m, d])
    } else {
        select_546([c, d, b, g, e, f, k, n, o, p, h])
    }
}
/// n = 9, i = 1, d < i, e < f, e < g, e < h
fn select_548([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_147([c, a, d, e, f, g, h, i, b])
    } else {
        select_147([c, b, d, e, f, g, h, i, a])
    }
}
/// n = 10, i = 2, a < c, b < d, b < e, d < j, e < f, e < g, e < h, e < i
fn select_549([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_155([d, e, f, g, h, i, a, j])
    } else {
        select_227([a, b, c, e, f, g, h, i, d])
    }
}
/// n = 5, i = 2, c < d, d < e
fn select_550([a, b, c, d, e]: [usize; 5]) -> usize {
    if a < d {
        select_44([b, a, c, d])
    } else {
        select_11([b, d, a, e])
    }
}
/// n = 10, i = 3, a < c, a < d, b < e, e < f, f < g, f < h, f < i, f < j
fn select_551([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_22([a, g, h, i, j])
    } else {
        select_550([c, d, b, e, f])
    }
}
/// n = 11, i = 3, a < c, a < k, b < d, c < e, d < f, d < k, f < g, f < h, f < i, f < j
fn select_552([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_22([a, g, h, i, j])
    } else {
        select_237([c, b, e, d, f, k])
    }
}
/// n = 11, i = 3, a < k, b < d, c < e, e < f, e < k, f < g, f < h, f < i, f < j
fn select_553([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < a {
        select_551([b, c, a, d, e, f, g, h, i, j])
    } else {
        select_552([a, c, b, e, d, f, g, h, i, j, k])
    }
}
/// n = 11, i = 3, b < d, c < e, e < f, e < g, g < h, g < i, g < j, g < k
fn select_554([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_549([b, e, d, f, g, h, i, j, k, a])
    } else {
        select_553([a, b, c, d, e, g, h, i, j, k, f])
    }
}
/// n = 14, i = 3, b < d, c < e, e < f, e < g, e < h, g < l, g < m, g < n, h < i, h < j, h < k
fn select_555([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if g < h {
        select_554([a, b, c, d, e, f, g, h, l, m, n])
    } else {
        select_554([a, b, c, d, e, f, h, g, i, j, k])
    }
}
/// n = 16, i = 4, a < c, a < d, a < l, b < e, d < g, e < f, e < h, e < l, h < i, h < j, h < k, k < m, l < n, l < o, l < p
fn select_556([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if h < a {
        select_548([f, i, j, k, a, c, d, l, m])
    } else {
        select_555([c, d, b, g, e, f, h, l, n, o, p, i, j, k])
    }
}
/// n = 16, i = 4, a < c, a < d, a < m, b < e, d < g, e < f, e < h, e < i, e < m, h < l, i < j, i < k, m < n, m < o, m < p
fn select_557([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if h < i {
        select_547([a, b, c, d, e, f, g, h, l, i, m, j, k, n, o, p])
    } else {
        select_556([a, b, c, d, e, f, g, i, j, k, h, m, l, n, o, p])
    }
}
/// n = 16, i = 4, a < d, a < e, a < m, b < c, b < f, e < h, f < g, f < i, f < j, f < m, i < l, j < k, m < n, m < o, m < p
fn select_558([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if c < j {
        select_538([a, b, d, e, c, f, g, h, i, l, j, m, k, n, o, p])
    } else {
        select_557([a, b, d, e, f, g, h, i, j, c, k, l, m, n, o, p])
    }
}
/// n = 17, i = 4, a < d, a < e, b < c, b < f, e < h, f < g, f < i, f < j, f < k, i < o, j < n, k < l, k < m, k < p, p < q
fn select_559([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if k < a {
        select_509([c, g, i, j, k, l, m, n, o, p, a, d, e, q])
    } else {
        select_558([a, b, c, d, e, f, g, h, i, j, n, o, k, l, m, p])
    }
}
/// n = 17, i = 4, a < d, a < e, b < c, b < f, b < g, e < k, f < i, f < j, f < n, g < h, g < l, g < m, l < p, m < o, n < q
fn select_560([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if f < g {
        select_496([a, b, c, d, e, f, i, j, k, n, g, h, q, l, m, o, p])
    } else {
        select_559([a, b, c, d, e, g, h, k, l, m, f, i, j, o, p, n, q])
    }
}
/// n = 17, i = 4, a < f, b < e, c < d, c < g, c < h, g < j, g < k, g < n, h < i, h < l, h < m, l < p, m < o, n < q
fn select_561([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if a < b {
        select_560([a, c, d, f, b, g, h, i, j, k, e, l, m, n, o, p, q])
    } else {
        select_560([b, c, d, e, a, g, h, i, j, k, f, l, m, n, o, p, q])
    }
}
/// n = 17, i = 4, c < f, d < e, d < g, d < h, g < j, g < k, g < n, h < i, h < l, h < m, l < p, m < o, n < q
fn select_562([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if a < b {
        select_561([a, c, d, e, f, b, g, h, i, j, k, l, m, n, o, p, q])
    } else {
        select_561([b, c, d, e, f, a, g, h, i, j, k, l, m, n, o, p, q])
    }
}
/// n = 17, i = 4, e < f, e < g, e < h, g < j, g < k, g < n, h < i, h < l, h < m, l < p, m < o, n < q
fn select_563([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if a < b {
        select_562([c, d, a, e, f, b, g, h, i, j, k, l, m, n, o, p, q])
    } else {
        select_562([c, d, b, e, f, a, g, h, i, j, k, l, m, n, o, p, q])
    }
}
/// n = 8, i = 1, d < e, d < f, d < g, d < h
fn select_564([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_156([c, a, d, e, f, g, h, b])
    } else {
        select_156([c, b, d, e, f, g, h, a])
    }
}
/// n = 7, i = 1, d < e, d < f, d < g
fn select_565([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_149([c, a, d, e, f, g, b])
    } else {
        select_149([c, b, d, e, f, g, a])
    }
}
/// n = 8, i = 1, c < h, d < e, d < f, d < g
fn select_566([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_9([a, c, d, e, f, g, h, b])
    } else {
        select_9([b, c, d, e, f, g, h, a])
    }
}
/// n = 9, i = 2, b < e, b < f, b < i, c < d, c < g, c < i, g < h
fn select_567([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if b < c {
        select_565([a, e, f, c, d, g, i])
    } else {
        select_566([a, d, g, b, e, f, i, h])
    }
}
/// n = 12, i = 2, b < f, b < g, c < d, c < e, c < h, g < l, h < i, h < j, h < k
fn select_568([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < b {
        select_564([a, d, e, h, b, i, j, k])
    } else {
        select_567([a, c, b, f, d, e, g, l, h])
    }
}
/// n = 12, i = 2, b < h, c < g, d < e, d < f, d < i, i < j, i < k, i < l
fn select_569([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if b < c {
        select_568([a, b, d, e, f, h, c, i, j, k, l, g])
    } else {
        select_568([a, c, d, e, f, g, b, i, j, k, l, h])
    }
}
/// n = 10, i = 2, a < e, a < f, a < h, b < c, b < d, b < g, g < i, h < j
fn select_570([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_566([e, f, h, b, c, d, g, j])
    } else {
        select_566([c, d, g, a, e, f, h, i])
    }
}
/// n = 8, i = 2, a < e, a < h, b < c, b < d, b < f, b < h, f < g
fn select_571([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < a {
        select_173([c, d, f, a, g])
    } else {
        select_482([a, b, c, d, e, f, h])
    }
}
/// n = 11, i = 2, a < e, a < g, a < k, b < c, b < d, b < f, b < k, f < h, g < i, g < j
fn select_572([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < g {
        select_571([a, b, c, d, e, f, h, k])
    } else {
        select_483([b, a, e, c, d, g, i, j, k])
    }
}
/// n = 11, i = 2, a < h, a < k, b < f, b < g, c < d, c < e, c < i, c < k, i < j
fn select_573([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < a {
        select_570([b, c, d, e, f, g, i, a, j, h])
    } else {
        select_572([a, c, d, e, h, i, b, j, f, g, k])
    }
}
/// n = 8, i = 2, a < c, a < h, b < d, b < e, b < h, d < g, e < f
fn select_574([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_242([a, b, c, d, e, g, h])
    } else {
        select_242([a, b, c, e, d, f, h])
    }
}
/// n = 8, i = 2, a < e, a < h, b < c, b < d, b < h, d < f, e < g
fn select_575([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_11([c, d, a, f])
    } else {
        select_150([b, a, c, e, g, d, h])
    }
}
/// n = 10, i = 2, a < c, a < f, a < j, b < d, b < e, b < j, d < h, e < g, f < i
fn select_576([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < f {
        select_574([a, b, c, d, e, g, h, j])
    } else {
        select_575([b, a, c, f, e, i, g, j])
    }
}
/// n = 10, i = 2, a < e, a < g, a < j, b < c, b < d, b < f, b < j, f < h, g < i
fn select_577([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_576([a, b, e, c, f, g, h, d, i, j])
    } else {
        select_576([a, b, e, d, f, g, h, c, i, j])
    }
}
/// n = 8, i = 2, a < c, a < d, a < h, b < e, b < h, e < f, e < g
fn select_578([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < e {
        select_73([c, d, b, h])
    } else {
        select_242([a, b, d, e, f, g, h])
    }
}
/// n = 9, i = 2, a < c, a < d, a < i, b < e, b < f, b < i, e < h, f < g
fn select_579([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < f {
        select_578([a, b, c, d, e, f, h, i])
    } else {
        select_578([a, b, c, d, f, e, g, i])
    }
}
/// n = 10, i = 2, a < f, a < g, b < c, b < d, b < e, e < h, f < j, g < i
fn select_580([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_173([c, d, e, a, h])
    } else {
        select_579([b, a, c, d, f, g, i, j, e])
    }
}
/// n = 11, i = 2, a < h, b < f, b < k, c < d, c < e, c < g, c < k, g < i, h < j
fn select_581([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < a {
        select_577([b, c, d, e, f, g, a, i, h, k])
    } else {
        select_580([a, c, d, e, g, b, h, i, j, f])
    }
}
/// n = 11, i = 2, b < h, c < g, c < k, d < e, d < f, d < i, d < k, i < j
fn select_582([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < a {
        select_573([c, b, d, e, f, a, h, g, i, j, k])
    } else {
        select_581([a, c, d, e, f, g, i, b, j, h, k])
    }
}
/// n = 8, i = 2, a < h, b < e, b < h, c < d, c < f, f < g
fn select_583([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < f {
        select_529([a, b, c, d, e, f, h])
    } else {
        select_20([b, c, d, e, f, a, g])
    }
}
/// n = 10, i = 2, a < d, a < e, b < c, b < f, e < j, f < g, f < h, f < i
fn select_584([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_49([c, f, a, g, h, i])
    } else {
        select_39([b, a, d, c, e, j, f])
    }
}
/// n = 10, i = 2, b < e, b < f, c < d, c < g, f < j, g < h, g < i
fn select_585([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < g {
        select_583([a, c, b, e, d, f, j, g])
    } else {
        select_584([b, c, d, e, f, g, a, h, i, j])
    }
}
/// n = 11, i = 3, a < f, a < g, b < e, b < h, c < d, c < g, c < h, g < k, h < i, h < j
fn select_586([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_82([f, b, c, d, e, g, k, h])
    } else {
        select_540([e, a, c, d, f, h, i, j, g])
    }
}
/// n = 11, i = 3, a < f, b < e, b < i, c < d, c < g, c < i, g < h, i < j, i < k
fn select_587([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_585([d, g, b, e, h, a, i, j, k, f])
    } else {
        select_586([a, b, c, d, e, f, g, i, j, k, h])
    }
}
/// n = 12, i = 3, a < f, b < e, b < l, c < d, c < g, c < h, g < k, h < i, h < j, h < l
fn select_588([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < a {
        select_582([d, g, b, h, i, j, e, k, a, f, l])
    } else {
        select_587([b, a, c, d, f, e, g, k, h, i, j])
    }
}
/// n = 14, i = 3, a < f, b < e, c < d, c < g, c < h, g < k, h < i, h < j, h < l, l < m, l < n
fn select_589([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if l < a {
        select_569([d, b, g, h, i, j, k, e, l, a, m, n])
    } else {
        select_588([b, a, c, d, f, e, g, h, i, j, k, l])
    }
}
/// n = 12, i = 2, b < e, b < g, b < l, c < d, c < f, c < l, f < h, f < i, g < j, g < k
fn select_590([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if b < c {
        select_8([a, e, g, c, d, f, l, j, k])
    } else {
        select_8([a, d, f, b, e, g, l, h, i])
    }
}
/// n = 14, i = 2, b < e, b < h, c < d, c < f, c < g, f < k, f < l, g < i, g < j, h < m, h < n
fn select_591([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if f < b {
        select_8([a, d, g, f, b, k, l, i, j])
    } else {
        select_590([a, b, c, d, e, g, h, i, j, m, n, f])
    }
}
/// n = 10, i = 1, c < h, c < i, c < j, d < e, d < f, d < g
fn select_592([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_541([a, b, c, d, h, i, j])
    } else {
        select_541([a, b, d, c, e, f, g])
    }
}
/// n = 12, i = 1, c < k, c < l, d < i, d < j, e < f, e < g, e < h
fn select_593([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if c < d {
        select_592([a, b, c, e, f, g, h, d, k, l])
    } else {
        select_592([a, b, d, e, f, g, h, c, i, j])
    }
}
/// n = 11, i = 2, b < e, c < d, c < f, c < g, f < k, g < h, g < i, g < j
fn select_594([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < b {
        select_8([a, d, f, g, h, i, j, b, k])
    } else {
        select_543([a, b, c, d, e, g, h, i, j, f])
    }
}
/// n = 16, i = 3, a < d, a < e, a < i, b < c, b < f, b < i, e < h, f < g, f < j, f < k, i < p, j < n, j < o, k < l, k < m
fn select_595([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if f < a {
        select_593([c, g, j, k, a, d, e, i, l, m, n, o])
    } else {
        select_594([d, e, b, c, h, i, f, g, j, k, p])
    }
}
/// n = 16, i = 3, a < d, a < f, b < c, b < e, b < g, e < i, f < j, g < h, g < k, g < l, k < o, k < p, l < m, l < n
fn select_596([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < a {
        select_591([c, e, g, h, i, k, l, a, m, n, o, p, d, f])
    } else {
        select_595([a, b, c, d, f, g, h, j, e, k, l, m, n, o, p, i])
    }
}
/// n = 16, i = 3, a < f, b < e, c < d, c < g, c < h, g < j, h < i, h < k, h < l, k < o, k < p, l < m, l < n
fn select_597([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_596([a, c, d, f, g, b, h, i, j, e, k, l, m, n, o, p])
    } else {
        select_596([b, c, d, e, g, a, h, i, j, f, k, l, m, n, o, p])
    }
}
/// n = 16, i = 3, a < f, b < e, c < d, c < g, c < h, c < i, g < m, h < k, h < l, i < j, i < n, n < o, n < p
fn select_598([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if h < i {
        select_589([a, b, c, d, e, f, g, h, k, l, m, i, j, n])
    } else {
        select_597([a, b, c, d, e, f, g, i, j, m, h, n, o, p, k, l])
    }
}
/// n = 16, i = 3, c < f, d < e, d < g, d < h, d < i, g < m, h < k, h < l, i < j, i < n, n < o, n < p
fn select_599([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_598([a, c, d, e, f, b, g, h, i, j, k, l, m, n, o, p])
    } else {
        select_598([b, c, d, e, f, a, g, h, i, j, k, l, m, n, o, p])
    }
}
/// n = 16, i = 3, e < f, e < g, e < h, e < i, g < m, h < k, h < l, i < j, i < n, n < o, n < p
fn select_600([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_599([c, d, a, e, f, b, g, h, i, j, k, l, m, n, o, p])
    } else {
        select_599([c, d, b, e, f, a, g, h, i, j, k, l, m, n, o, p])
    }
}
/// n = 8, i = 2, a < d, a < e, a < h, b < c, b < f, b < h, f < g
fn select_601([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < f {
        select_176([b, a, d, e, c, h])
    } else {
        select_39([a, b, c, e, f, g, h])
    }
}
/// n = 10, i = 2, a < d, a < e, b < c, b < f, b < g, f < j, g < h, g < i
fn select_602([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_149([c, f, g, a, h, i, j])
    } else {
        select_601([a, b, c, d, e, f, j, g])
    }
}
/// n = 11, i = 2, a < d, a < e, b < c, b < f, b < g, f < j, f < k, g < h, g < i
fn select_603([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_146([c, g, f, a, j, k, h, i])
    } else {
        select_483([a, b, c, d, e, g, h, i, f])
    }
}
/// n = 12, i = 2, a < f, a < g, b < e, b < h, c < d, c < i, h < l, i < j, i < k
fn select_604([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if b < c {
        select_602([a, b, e, f, g, h, c, d, i, l])
    } else {
        select_603([a, c, d, f, g, b, i, j, k, e, h])
    }
}
/// n = 12, i = 2, a < i, b < h, c < f, c < g, d < e, d < j, j < k, j < l
fn select_605([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_604([c, a, d, e, i, f, g, b, j, k, l, h])
    } else {
        select_604([c, b, d, e, h, f, g, a, j, k, l, i])
    }
}
/// n = 8, i = 2, b < h, c < d, c < h, d < e, d < f, d < g
fn select_606([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_418([a, c, b, d, e, f, g])
    } else {
        select_12([b, c, a, d, e, f, g, h])
    }
}
/// n = 9, i = 3, a < c, a < d, a < h, b < e, b < i, d < i, e < f, e < g, e < h
fn select_607([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_52([c, b, d, e, i])
    } else {
        select_482([a, e, f, g, c, d, h])
    }
}
/// n = 11, i = 3, a < c, a < d, a < h, b < e, b < h, b < k, d < k, e < f, e < g, h < i, h < j
fn select_608([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < e {
        select_606([c, d, b, h, e, i, j, k])
    } else {
        select_607([a, b, c, d, e, f, g, h, k])
    }
}
/// n = 12, i = 3, a < c, a < d, b < e, b < f, b < l, d < l, e < h, e < i, f < g, f < j, j < k
fn select_609([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < a {
        select_602([e, f, g, h, i, j, a, c, d, k])
    } else {
        select_608([a, b, c, d, e, h, i, f, g, j, l])
    }
}
/// n = 12, i = 3, a < c, a < f, b < d, b < e, b < g, b < l, d < k, e < j, f < l, g < h, g < i
fn select_610([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < e {
        select_609([a, b, c, f, g, d, k, h, i, e, j, l])
    } else {
        select_609([a, b, c, f, g, e, j, h, i, d, k, l])
    }
}
/// n = 15, i = 3, a < c, a < e, b < d, b < f, b < g, b < o, d < k, e < o, f < i, f < j, g < h, g < l, l < m, l < n
fn select_611([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if l < e {
        select_605([a, d, f, g, h, i, j, k, c, l, m, n])
    } else {
        select_610([a, b, c, d, g, e, f, i, j, h, k, o])
    }
}
/// n = 7, i = 2, a < e, b < c, b < d, b < f, f < g
fn select_612([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < a {
        select_173([c, d, f, a, g])
    } else {
        select_176([a, b, c, d, e, f])
    }
}
/// n = 10, i = 2, a < e, a < g, b < c, b < d, b < f, f < h, g < i, g < j
fn select_613([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < g {
        select_612([a, b, c, d, e, f, h])
    } else {
        select_481([b, a, e, c, d, g, i, j])
    }
}
/// n = 11, i = 2, a < d, a < f, a < k, b < c, b < e, b < k, e < g, e < h, f < i, f < j
fn select_614([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_40([a, b, c, d, e, g, h, k])
    } else {
        select_40([b, a, d, c, f, i, j, k])
    }
}
/// n = 11, i = 2, a < g, a < k, b < e, b < f, c < d, c < h, c < k, h < i, h < j
fn select_615([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < a {
        select_613([c, b, e, f, d, a, h, g, i, j])
    } else {
        select_614([a, c, d, g, h, b, i, j, e, f, k])
    }
}
/// n = 9, i = 1, b < h, b < i, c < d, c < e, c < f, c < g
fn select_616([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_23([a, c, d, e, f, g, b])
    } else {
        select_214([b, c, d, e, f, g, a, h, i])
    }
}
/// n = 12, i = 2, a < d, a < e, b < c, b < f, b < g, f < k, f < l, g < h, g < i, g < j
fn select_617([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < a {
        select_616([c, f, g, a, h, i, j, k, l])
    } else {
        select_483([a, b, c, d, e, f, k, l, g])
    }
}
/// n = 13, i = 2, a < g, b < e, b < f, c < d, c < h, c < i, h < l, h < m, i < j, i < k
fn select_618([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if a < h {
        select_615([a, b, c, d, e, f, g, i, j, k, h])
    } else {
        select_617([b, c, d, e, f, i, h, a, l, m, j, k])
    }
}
/// n = 8, i = 2, b < d, b < h, c < e, c < h, e < f, e < g
fn select_619([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_79([a, c, b, d, h, e])
    } else {
        select_12([b, c, d, e, a, f, g, h])
    }
}
/// n = 7, i = 3, a < f, a < g, b < e, b < f, c < d, c < e, d < g
fn select_620([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_84([b, d, e, a, g])
    } else {
        select_108([b, a, c, e, f, d, g])
    }
}
/// n = 9, i = 3, a < e, a < f, b < f, b < g, c < d, c < e, c < g, g < h, g < i
fn select_621([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < g {
        select_620([b, a, c, d, e, f, g])
    } else {
        select_419([a, b, c, e, f, g, d, h, i])
    }
}
/// n = 10, i = 3, a < f, b < f, b < g, b < j, c < d, c < e, c < g, e < j, g < h, g < i
fn select_622([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_619([d, e, b, a, g, h, i, j])
    } else {
        select_621([a, b, c, d, e, f, g, h, i])
    }
}
/// n = 9, i = 2, a < e, b < c, b < d, b < f, f < g, f < h, f < i
fn select_623([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_379([a, b, e, c, f, g, h, i, d])
    } else {
        select_379([a, b, e, d, f, g, h, i, c])
    }
}
/// n = 10, i = 3, a < f, b < f, b < g, c < d, c < g, d < e, g < h, g < i, g < j
fn select_624([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_377([d, b, a, e, g, h, i, j])
    } else {
        select_219([a, b, c, f, d, g, h, i, j, e])
    }
}
/// n = 10, i = 3, a < f, b < f, b < g, c < d, c < e, c < g, g < h, g < i, g < j
fn select_625([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_624([a, b, c, d, e, f, g, h, i, j])
    } else {
        select_624([a, b, c, e, d, f, g, h, i, j])
    }
}
/// n = 10, i = 3, a < i, b < d, b < e, b < j, c < f, c < i, f < g, f < h, f < j
fn select_626([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < b {
        select_623([a, f, g, h, i, b, d, e, j])
    } else {
        select_625([a, c, b, d, e, i, f, g, h, j])
    }
}
/// n = 12, i = 3, a < i, b < d, b < e, b < j, c < f, c < i, c < j, f < g, f < h, j < k, j < l
fn select_627([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < j {
        select_626([a, b, c, d, e, f, g, h, i, j])
    } else {
        select_625([a, c, b, d, e, i, j, f, k, l])
    }
}
/// n = 13, i = 3, a < i, b < d, b < e, b < j, c < f, c < i, c < j, c < m, e < m, f < g, f < h, j < k, j < l
fn select_628([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if m < f {
        select_622([a, c, b, d, e, i, j, k, l, m])
    } else {
        select_627([a, b, c, d, e, f, g, h, i, j, k, l])
    }
}
/// n = 15, i = 3, a < k, b < d, b < e, c < f, c < g, c < k, c < o, e < o, f < i, f < j, g < h, g < l, l < m, l < n
fn select_629([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < b {
        select_618([a, f, g, h, i, j, k, b, l, m, n, d, e])
    } else {
        select_628([a, b, c, d, e, f, i, j, k, g, h, l, o])
    }
}
/// n = 15, i = 3, b < e, b < f, c < d, c < g, c < h, c < o, f < o, g < j, g < k, h < i, h < l, l < m, l < n
fn select_630([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if d < a {
        select_611([b, c, e, d, f, g, h, i, j, k, a, l, m, n, o])
    } else {
        select_629([a, b, c, e, f, g, h, i, j, k, d, l, m, n, o])
    }
}
/// n = 8, i = 2, a < d, b < c, b < e, d < h, e < f, e < g
fn select_631([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_18([c, e, a, f, g])
    } else {
        select_90([b, a, c, d, h, e])
    }
}
/// n = 8, i = 2, a < c, b < d, b < e, d < h, e < f, e < g
fn select_632([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_24([d, e, a, f, g, h])
    } else {
        select_90([a, b, c, d, h, e])
    }
}
/// n = 11, i = 2, a < c, a < f, b < d, b < e, d < i, e < g, e < h, f < j, f < k
fn select_633([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < e {
        select_631([b, a, c, d, f, j, k, i])
    } else {
        select_632([a, b, c, d, e, g, h, i])
    }
}
/// n = 12, i = 2, a < c, a < d, a < f, a < l, b < e, b < g, b < l, e < j, f < k, g < h, g < i
fn select_634([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_566([c, d, f, b, e, g, l, k])
    } else {
        select_502([e, g, a, c, d, f, l, h, i, j])
    }
}
/// n = 12, i = 2, a < f, b < d, b < e, b < l, c < g, c < h, c < l, g < k, h < i, h < j
fn select_635([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_633([a, c, f, g, h, b, i, j, k, d, e])
    } else {
        select_634([b, c, d, e, g, a, h, i, j, k, f, l])
    }
}
/// n = 10, i = 3, a < d, a < g, b < c, b < g, b < i, b < j, c < f, d < e, d < i, d < j, g < h
fn select_636([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < c {
        select_152([d, b, e, g, c, h, i, j])
    } else {
        select_245([a, b, c, d, e, f, i, j, g])
    }
}
/// n = 12, i = 3, a < d, a < g, a < h, b < c, b < g, b < h, b < l, c < f, d < e, d < l, g < k, h < i, h < j
fn select_637([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < d {
        select_379([c, a, f, g, h, d, i, j, k])
    } else {
        select_636([a, b, c, d, e, f, g, k, h, l])
    }
}
/// n = 14, i = 3, a < d, a < j, a < k, b < c, b < e, b < j, b < k, c < h, d < i, e < f, e < g, j < n, k < l, k < m
fn select_638([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if e < d {
        select_635([c, e, a, f, g, h, j, k, l, m, n, d])
    } else {
        select_637([a, b, c, d, i, h, j, k, l, m, n, e])
    }
}
/// n = 16, i = 3, a < d, a < l, b < c, b < e, b < f, b < l, c < j, d < k, e < h, e < i, f < g, f < m, l < p, m < n, m < o
fn select_639([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if f < a {
        select_618([c, e, f, g, h, i, j, a, m, n, o, d, l])
    } else {
        select_638([a, b, c, d, e, h, i, j, k, l, f, g, m, p])
    }
}
/// n = 12, i = 3, a < c, a < i, a < l, b < d, b < i, c < g, d < e, d < f, d < h, d < l, h < j, i < k
fn select_640([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < a {
        select_566([e, f, h, a, c, i, l, j])
    } else {
        select_549([c, b, g, i, d, e, f, h, l, k])
    }
}
/// n = 14, i = 3, a < c, a < i, a < j, b < d, b < i, b < j, c < g, d < e, d < f, d < h, h < k, i < n, j < l, j < m
fn select_641([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if j < d {
        select_379([c, b, g, i, j, d, l, m, n])
    } else {
        select_640([a, b, c, d, e, f, g, h, i, k, n, j])
    }
}
/// n = 12, i = 3, a < f, a < h, a < l, b < d, b < g, b < l, c < f, c < g, c < h, c < l, d < e, g < i, h < j, h < k
fn select_642([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < d {
        select_359([b, a, f, g, h, j, k, i, l])
    } else {
        select_168([a, c, b, d, e, f, g, i, l])
    }
}
/// n = 14, i = 3, a < f, a < i, b < d, b < g, b < h, c < f, c < g, c < h, c < i, d < e, g < l, h < j, h < k, i < m, i < n
fn select_643([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if h < a {
        select_379([d, c, e, g, h, a, j, k, l])
    } else {
        select_642([a, b, c, d, e, f, g, i, l, m, n, h])
    }
}
/// n = 14, i = 3, a < i, b < d, b < j, b < k, c < e, c < i, c < j, c < k, d < h, e < f, e < g, j < n, k < l, k < m
fn select_644([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if e < a {
        select_641([b, c, d, e, f, g, h, a, j, k, i, l, m, n])
    } else {
        select_643([a, b, c, d, h, i, j, k, e, l, m, n, f, g])
    }
}
/// n = 16, i = 3, a < k, b < d, b < l, c < e, c < f, c < k, c < l, d < j, e < h, e < i, f < g, f < m, l < p, m < n, m < o
fn select_645([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if f < b {
        select_618([a, e, f, g, h, i, k, b, m, n, o, d, l])
    } else {
        select_644([a, b, c, d, e, h, i, j, k, l, f, g, m, p])
    }
}
/// n = 16, i = 3, b < e, b < l, c < d, c < f, c < g, c < l, e < k, f < i, f < j, g < h, g < m, l < p, m < n, m < o
fn select_646([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if d < a {
        select_639([b, c, d, e, f, g, h, i, j, a, k, l, m, n, o, p])
    } else {
        select_645([a, b, c, e, f, g, h, i, j, k, d, l, m, n, o, p])
    }
}
/// n = 16, i = 3, b < f, c < l, d < e, d < g, d < h, d < l, g < j, g < k, h < i, h < m, l < p, m < n, m < o
fn select_647([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if b < c {
        select_630([a, b, d, e, f, c, g, h, i, j, k, m, n, o, l])
    } else {
        select_646([a, c, d, e, b, g, h, i, j, k, f, l, m, n, o, p])
    }
}
/// n = 16, i = 3, d < l, e < f, e < g, e < h, e < l, g < j, g < k, h < i, h < m, l < p, m < n, m < o
fn select_648([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_647([c, a, d, e, f, b, g, h, i, j, k, l, m, n, o, p])
    } else {
        select_647([c, b, d, e, f, a, g, h, i, j, k, l, m, n, o, p])
    }
}
/// n = 8, i = 3, b < d, b < g, c < e, c < g, e < f, g < h
fn select_649([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if g < a {
        select_20([e, b, d, f, g, a, h])
    } else {
        select_344([a, b, c, d, e, f, g])
    }
}
/// n = 8, i = 3, b < f, c < g, d < e, d < g, g < h
fn select_650([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < c {
        select_106([a, d, b, f, e, c, g])
    } else {
        select_649([a, d, c, e, b, f, g, h])
    }
}
/// n = 11, i = 3, a < e, b < f, b < g, c < d, c < f, c < g, f < k, g < h, g < i, g < j
fn select_651([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_156([d, f, g, a, h, i, j, k])
    } else {
        select_257([a, b, c, d, e, f, k, g])
    }
}
/// n = 11, i = 3, c < f, c < g, d < e, d < f, d < g, f < k, g < h, g < i, g < j
fn select_652([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_651([a, c, d, e, b, f, g, h, i, j, k])
    } else {
        select_651([b, c, d, e, a, f, g, h, i, j, k])
    }
}
/// n = 12, i = 3, b < f, c < g, c < h, d < e, d < g, d < h, g < l, h < i, h < j, h < k
fn select_653([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < h {
        select_650([a, b, c, d, e, f, g, l])
    } else {
        select_652([a, b, c, d, e, g, h, i, j, k, l])
    }
}
/// n = 12, i = 3, d < g, d < h, e < f, e < g, e < h, g < l, h < i, h < j, h < k
fn select_654([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_653([c, a, d, e, f, b, g, h, i, j, k, l])
    } else {
        select_653([c, b, d, e, f, a, g, h, i, j, k, l])
    }
}
/// n = 9, i = 1, b < g, b < h, b < i, c < d, c < e, c < f
fn select_655([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if b < c {
        select_49([a, b, c, g, h, i])
    } else {
        select_49([a, c, b, d, e, f])
    }
}
/// n = 11, i = 2, a < d, b < c, b < e, b < f, e < j, e < k, f < g, f < h, f < i
fn select_656([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_655([c, e, f, g, h, i, a, j, k])
    } else {
        select_50([a, b, c, d, f, g, h, i, e])
    }
}
/// n = 11, i = 2, c < d, c < e, c < f, e < j, e < k, f < g, f < h, f < i
fn select_657([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_656([a, c, d, b, e, f, g, h, i, j, k])
    } else {
        select_656([b, c, d, a, e, f, g, h, i, j, k])
    }
}
/// n = 12, i = 2, c < d, c < e, c < f, c < g, e < l, f < k, g < h, g < i, g < j
fn select_658([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < f {
        select_657([a, b, c, d, e, g, h, i, j, f, l])
    } else {
        select_657([a, b, c, d, f, g, h, i, j, e, k])
    }
}
/// n = 9, i = 2, a < d, a < e, b < c, b < f, e < i, f < g, f < h
fn select_659([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_18([c, f, a, g, h])
    } else {
        select_39([b, a, d, c, e, i, f])
    }
}
/// n = 10, i = 2, a < d, a < g, b < c, b < e, b < f, e < i, f < h, g < j
fn select_660([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_659([a, b, c, d, g, e, f, i, j])
    } else {
        select_659([a, b, c, d, g, f, e, h, j])
    }
}
/// n = 11, i = 2, a < d, a < g, a < k, b < c, b < e, b < f, b < k, e < i, f < h, g < j
fn select_661([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_41([a, b, c, d, g, e, f, i, j, k])
    } else {
        select_41([a, b, c, d, g, f, e, h, j, k])
    }
}
/// n = 11, i = 2, a < f, b < e, b < k, c < d, c < g, c < h, c < k, g < j, h < i
fn select_662([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_660([a, c, d, f, g, h, b, i, j, e])
    } else {
        select_661([b, c, d, e, g, h, a, i, j, f, k])
    }
}
/// n = 7, i = 3, a < d, a < g, b < c, b < g, c < e, d < f
fn select_663([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < d {
        select_19([a, c, e, g, d])
    } else {
        select_19([b, d, f, g, c])
    }
}
/// n = 10, i = 3, a < c, a < g, b < d, b < g, c < f, d < e, d < h, h < i, h < j
fn select_664([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < c {
        select_20([a, d, e, g, h, i, j])
    } else {
        select_663([a, b, d, c, e, f, g])
    }
}
/// n = 11, i = 3, a < c, a < g, b < d, b < g, c < f, d < e, d < h, d < i, h < k, i < j
fn select_665([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < i {
        select_664([a, b, c, d, e, f, g, h, i, k])
    } else {
        select_664([a, b, c, d, e, f, g, i, h, j])
    }
}
/// n = 11, i = 3, a < c, a < d, a < j, b < e, b < k, d < k, e < f, e < g, e < j, g < h, g < i
fn select_666([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < d {
        select_40([a, e, f, c, g, h, i, j])
    } else {
        select_53([b, a, c, d, e, f, j, k])
    }
}
/// n = 12, i = 3, a < c, a < d, a < k, b < e, b < l, d < l, e < f, e < g, e < h, e < k, g < j, h < i
fn select_667([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < h {
        select_666([a, b, c, d, e, f, g, h, j, k, l])
    } else {
        select_666([a, b, c, d, e, f, h, g, i, k, l])
    }
}
/// n = 12, i = 3, a < g, b < d, b < l, c < e, c < g, e < f, e < h, e < i, e < l, h < k, i < j
fn select_668([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_665([a, c, b, e, f, d, g, h, i, j, k])
    } else {
        select_667([b, c, d, a, e, f, h, i, j, k, l, g])
    }
}
/// n = 12, i = 3, b < e, b < l, c < d, c < f, f < g, f < h, f < i, f < l, h < k, i < j
fn select_669([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < a {
        select_662([d, b, f, g, e, a, h, i, j, k, l])
    } else {
        select_668([a, b, c, e, f, g, d, h, i, j, k, l])
    }
}
/// n = 14, i = 3, b < e, c < d, c < f, f < g, f < h, f < i, f < j, h < n, i < m, j < k, j < l
fn select_670([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if j < b {
        select_658([a, d, f, g, h, i, j, b, k, l, m, n])
    } else {
        select_669([a, b, c, d, e, f, g, h, i, m, n, j])
    }
}
/// n = 14, i = 3, d < e, d < f, f < g, f < h, f < i, f < j, h < n, i < m, j < k, j < l
fn select_671([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if a < b {
        select_670([c, a, d, e, b, f, g, h, i, j, k, l, m, n])
    } else {
        select_670([c, b, d, e, a, f, g, h, i, j, k, l, m, n])
    }
}
/// n = 15, i = 3, d < j, e < f, e < g, e < j, g < h, g < i, g < k, i < n, j < o, k < l, k < m
fn select_672([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if d < g {
        select_654([a, b, c, d, e, f, j, g, h, i, k, o])
    } else {
        select_671([a, b, c, e, f, g, h, d, i, k, l, m, n, j])
    }
}
/// n = 8, i = 2, a < e, a < f, b < c, b < d, b < g, g < h
fn select_673([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if g < a {
        select_173([c, d, g, a, h])
    } else {
        select_514([a, b, c, d, e, f, g])
    }
}
/// n = 10, i = 2, a < e, a < i, a < j, b < c, b < d, b < i, b < j, c < g, d < f, e < h
fn select_674([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_309([a, b, e, c, d, g, h, i, j])
    } else {
        select_309([a, b, e, d, c, f, h, i, j])
    }
}
/// n = 10, i = 2, a < f, a < i, a < j, b < c, b < d, b < e, b < i, b < j, e < g, f < h
fn select_675([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_674([a, b, c, e, f, g, d, h, i, j])
    } else {
        select_674([a, b, d, e, f, g, c, h, i, j])
    }
}
/// n = 10, i = 2, a < f, b < i, b < j, c < d, c < e, c < g, c < i, c < j, g < h
fn select_676([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_673([a, c, d, e, b, f, g, h])
    } else {
        select_675([b, c, d, e, g, a, h, f, i, j])
    }
}
/// n = 10, i = 2, c < i, c < j, d < e, d < f, d < g, d < i, d < j, g < h
fn select_677([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_676([a, c, d, e, f, b, g, h, i, j])
    } else {
        select_676([b, c, d, e, f, a, g, h, i, j])
    }
}
/// n = 10, i = 2, a < c, a < e, b < d, b < f, d < i, e < j, f < g, f < h
fn select_678([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_24([d, f, a, g, h, i])
    } else {
        select_575([b, a, c, e, d, j, i, f])
    }
}
/// n = 10, i = 2, a < e, b < d, c < f, c < g, f < j, g < h, g < i
fn select_679([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_678([a, c, e, f, b, g, h, i, j, d])
    } else {
        select_678([b, c, d, f, a, g, h, i, j, e])
    }
}
/// n = 10, i = 2, c < e, d < f, d < g, f < j, g < h, g < i
fn select_680([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_679([a, c, d, e, b, f, g, h, i, j])
    } else {
        select_679([b, c, d, e, a, f, g, h, i, j])
    }
}
/// n = 10, i = 2, e < f, e < g, f < j, g < h, g < i
fn select_681([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_680([c, d, a, e, b, f, g, h, i, j])
    } else {
        select_680([c, d, b, e, a, f, g, h, i, j])
    }
}
/// n = 11, i = 3, c < g, c < h, d < e, d < f, d < h, d < j, d < k, g < j, g < k, h < i
fn select_682([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < d {
        select_677([a, b, g, d, e, f, h, i, j, k])
    } else {
        select_681([a, b, e, f, c, h, g, j, k, i])
    }
}
/// n = 8, i = 4, a < g, b < g, c < e, d < f, d < g, e < f, g < h
fn select_683([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_311([b, c, d, e, g, h, f])
    } else {
        select_306([a, b, d, f])
    }
}
/// n = 7, i = 3, a < e, b < e, c < f, d < f, f < g
fn select_684([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < a {
        select_131([a, b, d, f, g, e])
    } else {
        select_104([c, d, b, e, f])
    }
}
/// n = 8, i = 4, a < f, b < g, c < g, d < e, d < g, g < h
fn select_685([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < e {
        select_683([b, c, a, d, f, e, g, h])
    } else {
        select_684([a, e, b, c, f, g, h])
    }
}
/// n = 6, i = 2, c < d, d < e, d < f
fn select_686([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_237([a, c, b, d, e, f])
    } else {
        select_237([b, c, a, d, e, f])
    }
}
/// n = 8, i = 3, a < h, b < d, b < g, c < e, e < f, e < g, e < h
fn select_687([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < b {
        select_316([f, a, b, d, g, h])
    } else {
        select_686([a, d, c, e, f, g])
    }
}
/// n = 8, i = 3, b < d, b < h, c < e, e < f, e < g, e < h
fn select_688([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < a {
        select_39([b, e, g, d, f, a, h])
    } else {
        select_687([a, b, c, d, e, g, h, f])
    }
}
/// n = 9, i = 4, b < f, b < i, c < g, d < e, d < g, g < h, g < i
fn select_689([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < g {
        select_685([b, a, c, d, e, f, g, h])
    } else {
        select_688([e, b, c, f, g, a, h, i])
    }
}
/// n = 12, i = 4, c < f, c < i, d < e, d < g, f < k, f < l, g < h, g < i, g < k, g < l, i < j
fn select_690([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < a {
        select_682([b, e, c, g, a, h, f, i, j, k, l])
    } else {
        select_689([b, c, a, d, e, f, g, h, i])
    }
}
/// n = 7, i = 3, a < e, b < f, c < d, c < f, f < g
fn select_691([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < e {
        select_550([a, d, b, f, g])
    } else {
        select_384([b, a, c, d, e])
    }
}
/// n = 8, i = 3, a < h, b < e, b < g, c < d, c < f, f < g, f < h
fn select_692([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < a {
        select_397([d, b, f, e, a, h, g])
    } else {
        select_691([b, a, c, d, e, f, h])
    }
}
/// n = 8, i = 2, a < d, a < f, b < c, b < e, e < g, f < h
fn select_693([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_62([a, b, c, d, e, g])
    } else {
        select_62([b, a, d, c, f, h])
    }
}
/// n = 7, i = 2, a < e, b < c, b < d, d < f, e < g
fn select_694([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_11([c, d, a, f])
    } else {
        select_90([b, a, c, e, g, d])
    }
}
/// n = 7, i = 3, a < e, b < e, b < f, c < d, c < f, f < g
fn select_695([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < d {
        select_237([a, c, e, f, d, g])
    } else {
        select_96([a, b, c, d, e, f])
    }
}
/// n = 9, i = 3, a < e, a < g, b < d, b < f, c < e, c < f, c < g, f < h, g < i
fn select_696([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < d {
        select_694([b, a, e, g, f, i, h])
    } else {
        select_695([a, c, b, d, e, f, h])
    }
}
/// n = 9, i = 3, a < g, b < d, b < h, c < e, c < g, c < h, e < f, h < i
fn select_697([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_693([b, e, f, d, a, h, g, i])
    } else {
        select_696([a, b, c, d, g, h, e, i, f])
    }
}
/// n = 9, i = 3, a < g, b < f, c < g, c < h, d < e, d < h, h < i
fn select_698([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if b < c {
        select_692([a, d, b, f, e, c, h, g])
    } else {
        select_697([a, d, c, e, b, f, g, h, i])
    }
}
/// n = 9, i = 2, a < c, a < d, b < e, b < f, e < i, f < g, f < h
fn select_699([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_24([e, f, a, g, h, i])
    } else {
        select_423([b, a, c, d, e, i, f])
    }
}
/// n = 11, i = 3, a < d, a < f, b < d, b < e, b < g, c < e, c < f, c < g, e < j, f < k, g < h, g < i
fn select_700([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_24([e, g, a, h, i, j])
    } else {
        select_167([a, b, c, d, e, f, j, k, g])
    }
}
/// n = 11, i = 3, a < f, b < f, b < g, b < h, c < d, c < g, c < h, d < e, g < k, h < i, h < j
fn select_701([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_699([d, b, a, e, g, h, i, j, k])
    } else {
        select_700([a, b, c, f, g, d, h, i, j, k, e])
    }
}
/// n = 8, i = 3, a < f, a < h, b < e, b < f, c < d, c < e, d < h, f < g
fn select_702([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < f {
        select_104([a, d, b, e, h])
    } else {
        select_84([c, a, e, f, g])
    }
}
/// n = 11, i = 3, a < d, a < e, b < f, b < g, b < k, c < e, c < f, c < g, d < k, f < j, g < h, g < i
fn select_703([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < d {
        select_632([a, b, e, f, g, h, i, j])
    } else {
        select_702([b, c, a, d, e, f, j, k])
    }
}
/// n = 11, i = 3, a < f, b < e, c < f, c < g, c < h, d < e, d < g, d < h, g < k, h < i, h < j
fn select_704([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_703([a, d, c, b, f, g, h, i, j, k, e])
    } else {
        select_703([b, c, d, a, e, g, h, i, j, k, f])
    }
}
/// n = 11, i = 3, b < f, c < f, c < g, c < h, d < e, d < g, d < h, g < k, h < i, h < j
fn select_705([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_701([b, c, d, e, a, f, g, h, i, j, k])
    } else {
        select_704([a, b, d, c, f, e, g, h, i, j, k])
    }
}
/// n = 12, i = 3, a < g, b < f, c < g, c < h, c < i, d < e, d < h, d < i, h < l, i < j, i < k
fn select_706([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < i {
        select_698([a, b, c, d, e, f, g, h, l])
    } else {
        select_705([b, a, c, d, e, g, h, i, j, k, l])
    }
}
/// n = 10, i = 3, a < c, a < g, a < j, b < d, b < g, c < f, d < e, d < h, d < j, h < i
fn select_707([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < c {
        select_39([a, d, e, g, h, i, j])
    } else {
        select_51([b, a, c, d, e, f, g, j])
    }
}
/// n = 9, i = 3, a < c, a < h, b < d, b < i, c < e, c < i, d < f, d < h, f < g
fn select_708([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_11([e, b, d, i])
    } else {
        select_27([f, a, c, h, g])
    }
}
/// n = 10, i = 4, a < f, a < g, a < j, b < d, b < j, c < e, d < f, d < i, e < g, e < i, e < j, g < h
fn select_709([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < d {
        select_72([b, g, h, j])
    } else {
        select_95([a, d, c, e, f, i, j])
    }
}
/// n = 11, i = 4, a < f, a < g, a < k, b < d, b < f, b < k, c < e, c < j, d < i, e < g, e < i, e < k, f < j, g < h
fn select_710([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < d {
        select_708([b, c, f, e, d, g, h, k, j])
    } else {
        select_709([a, b, c, d, e, f, g, h, i, k])
    }
}
/// n = 11, i = 4, a < d, a < g, a < k, b < g, b < h, b < k, c < e, c < j, e < f, e < h, e < k, g < j, h < i
fn select_711([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < d {
        select_136([a, b, e, f, h, g, i, j, d, k])
    } else {
        select_710([b, a, c, d, e, g, h, i, f, j, k])
    }
}
/// n = 12, i = 4, a < d, a < l, b < e, b < i, b < l, c < f, c < h, e < h, e < k, f < g, f < i, f < k, f < l, i < j
fn select_712([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < a {
        select_707([e, c, a, f, g, d, h, i, j, k])
    } else {
        select_711([a, b, c, d, f, g, e, i, j, h, l])
    }
}
/// n = 14, i = 4, a < d, b < e, b < i, b < j, c < f, c < h, e < h, e < n, f < g, f < i, f < j, f < n, i < m, j < k, j < l
fn select_713([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if j < a {
        select_157([e, f, g, h, i, j, a, k, l, m, n])
    } else {
        select_712([a, b, c, d, e, f, g, h, i, m, n, j])
    }
}
/// n = 14, i = 4, a < e, b < f, b < i, b < j, c < d, c < g, f < n, g < h, g < i, g < j, g < n, i < m, j < k, j < l
fn select_714([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if d < f {
        select_706([d, a, b, g, h, e, f, i, j, k, l, m])
    } else {
        select_713([a, b, c, e, f, g, h, d, i, j, k, l, m, n])
    }
}
/// n = 14, i = 4, c < f, c < i, c < j, d < e, d < g, f < n, g < h, g < i, g < j, g < n, i < m, j < k, j < l
fn select_715([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if a < b {
        select_714([a, c, d, e, b, f, g, h, i, j, k, l, m, n])
    } else {
        select_714([b, c, d, e, a, f, g, h, i, j, k, l, m, n])
    }
}
/// n = 15, i = 4, c < j, d < i, d < k, e < f, e < g, g < h, g < i, g < j, g < k, i < n, j < o, k < l, k < m
fn select_716([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if c < d {
        select_690([a, b, c, e, f, d, g, h, j, o, i, k])
    } else {
        select_715([a, b, d, e, f, c, g, h, i, k, l, m, n, j])
    }
}
/// n = 17, i = 4, c < l, d < k, e < f, e < g, g < h, g < i, g < k, g < l, i < j, i < m, k < p, l < q, m < n, m < o
fn select_717([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if i < c {
        select_672([a, b, f, d, g, h, i, j, c, k, m, n, o, l, p])
    } else {
        select_716([a, b, d, c, e, f, g, h, l, k, i, j, m, q, p])
    }
}
/// n = 17, i = 4, d < m, e < f, e < g, g < h, g < i, g < j, g < m, i < l, j < k, j < n, m < q, n < o, n < p
fn select_718([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if i < a {
        select_648([b, c, f, d, g, h, i, j, k, a, l, m, n, o, p, q])
    } else {
        select_717([b, c, a, d, e, f, g, h, j, k, m, i, n, o, p, q, l])
    }
}
/// n = 17, i = 4, e < f, e < g, g < h, g < i, g < j, g < k, i < n, j < m, k < l, k < o, o < p, o < q
fn select_719([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if i < a {
        select_600([b, c, d, f, g, h, j, i, k, l, a, n, m, o, p, q])
    } else {
        select_718([b, c, d, a, e, f, g, h, j, k, l, m, i, o, p, q, n])
    }
}
/// n = 11, i = 1, e < j, e < k, f < g, f < h, f < i
fn select_720([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_200([c, d, a, e, f, g, h, i, j, k, b])
    } else {
        select_200([c, d, b, e, f, g, h, i, j, k, a])
    }
}
/// n = 10, i = 2, a < j, b < d, c < e, c < j, e < f, e < g, e < h, e < i
fn select_721([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < a {
        select_118([b, c, a, d, e, f, g, h, i])
    } else {
        select_207([a, c, b, e, f, g, h, i, d, j])
    }
}
/// n = 10, i = 2, b < e, c < d, c < f, f < g, f < h, f < i, f < j
fn select_722([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < d {
        select_721([a, b, c, e, f, g, h, i, j, d])
    } else {
        select_549([b, c, e, d, f, g, h, i, j, a])
    }
}
/// n = 14, i = 3, b < d, b < j, c < e, c < j, d < i, e < f, e < g, e < h, e < k, k < l, k < m, k < n
fn select_723([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if e < b {
        select_720([a, f, g, h, b, k, l, m, n, d, j])
    } else {
        select_722([a, d, c, j, i, e, f, g, h, k])
    }
}
/// n = 11, i = 1, c < k, d < j, e < f, e < g, e < h, e < i
fn select_724([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < d {
        select_503([a, b, c, e, f, g, h, i, d, k])
    } else {
        select_503([a, b, d, e, f, g, h, i, c, j])
    }
}
/// n = 13, i = 3, b < d, b < h, b < m, c < e, c < h, d < g, e < f, e < i, e < j, e < m, i < l, j < k
fn select_725([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if e < b {
        select_463([a, f, i, j, b, d, h, m, k, l])
    } else {
        select_722([a, d, c, h, g, e, f, i, j, m])
    }
}
/// n = 16, i = 3, b < d, b < h, c < e, c < h, d < g, e < f, e < i, e < j, e < k, i < p, j < o, k < l, k < m, k < n
fn select_726([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if k < b {
        select_724([a, f, i, j, k, b, l, m, n, o, p])
    } else {
        select_725([a, b, c, d, e, f, g, h, i, j, o, p, k])
    }
}
/// n = 16, i = 3, b < d, b < l, c < e, c < f, c < l, d < k, e < h, e < i, e < j, f < g, f < m, f < n, m < p, n < o
fn select_727([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < f {
        select_723([a, b, c, d, e, h, i, j, k, l, f, g, m, n])
    } else {
        select_726([a, b, c, d, f, g, k, l, m, n, e, h, i, j, o, p])
    }
}
/// n = 14, i = 2, b < g, b < h, b < i, c < d, c < e, c < f, c < j, h < n, i < m, j < k, j < l
fn select_728([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if b < c {
        select_724([a, g, h, i, c, d, e, f, j, m, n])
    } else {
        select_720([a, d, e, f, j, b, g, h, i, k, l])
    }
}
/// n = 10, i = 3, a < d, b < e, c < e, c < j, d < j, e < f, e < g, e < h, e < i
fn select_729([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_22([a, f, g, h, i])
    } else {
        select_92([b, d, c, j, e])
    }
}
/// n = 10, i = 3, b < e, c < f, d < e, d < f, f < g, f < h, f < i, f < j
fn select_730([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_729([a, c, d, b, f, g, h, i, j, e])
    } else {
        select_335([b, c, d, a, e, f, g, h, i, j])
    }
}
/// n = 11, i = 3, c < f, c < k, d < e, d < f, e < k, f < g, f < h, f < i, f < j
fn select_731([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_175([b, e, c, a, f, g, h, i, j, k])
    } else {
        select_730([b, a, c, d, e, f, g, h, i, j])
    }
}
/// n = 14, i = 3, c < f, c < g, c < n, d < e, d < f, d < g, e < n, f < k, f < l, f < m, g < h, g < i, g < j
fn select_732([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if f < g {
        select_731([a, b, c, d, e, f, g, k, l, m, n])
    } else {
        select_731([a, b, c, d, e, g, f, h, i, j, n])
    }
}
/// n = 17, i = 4, b < e, b < f, b < k, c < g, c < k, c < q, d < f, d < g, d < k, f < q, g < h, g < i, g < j, i < m, j < l, k < n, k < o, k < p
fn select_733([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if g < b {
        select_463([a, h, i, j, b, e, f, k, l, m])
    } else {
        select_732([a, e, c, d, f, g, k, n, o, p, h, i, j, q])
    }
}
/// n = 17, i = 4, b < e, b < f, c < g, c < h, c < q, d < f, d < g, d < h, f < q, g < j, g < k, g < l, h < i, h < m, h < n, m < p, n < o
fn select_734([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if g < b {
        select_728([a, h, g, j, k, l, i, m, n, b, e, f, o, p])
    } else {
        select_733([a, b, c, d, e, f, h, i, m, n, g, o, p, j, k, l, q])
    }
}
/// n = 17, i = 4, b < e, c < g, c < h, c < m, d < f, d < g, d < h, f < m, g < j, g < k, g < l, h < i, h < n, h < o, n < q, o < p
fn select_735([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if f < b {
        select_727([a, f, c, b, g, h, i, j, k, l, e, m, n, o, p, q])
    } else {
        select_734([a, b, c, d, e, f, g, h, i, j, k, l, n, o, p, q, m])
    }
}
/// n = 17, i = 4, d < g, d < h, d < m, e < f, e < g, e < h, f < m, g < j, g < k, g < l, h < i, h < n, h < o, n < q, o < p
fn select_736([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if a < b {
        select_735([c, a, d, e, b, f, g, h, i, j, k, l, m, n, o, p, q])
    } else {
        select_735([c, b, d, e, a, f, g, h, i, j, k, l, m, n, o, p, q])
    }
}
/// n = 17, i = 4, d < g, d < h, d < i, e < f, e < h, e < i, h < k, h < l, h < m, i < j, i < n, i < o, n < q, o < p
fn select_737([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if f < g {
        select_736([a, b, c, d, e, f, h, i, j, k, l, m, g, n, o, p, q])
    } else {
        select_736([a, b, c, e, d, g, h, i, j, k, l, m, f, n, o, p, q])
    }
}
/// n = 9, i = 1, d < h, d < i, e < f, e < g
fn select_738([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_565([a, b, c, d, e, h, i])
    } else {
        select_565([a, b, c, e, d, f, g])
    }
}
/// n = 7, i = 2, a < g, b < e, b < f, c < d, c < e, c < f, c < g
fn select_739([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_19([a, c, d, b, g])
    } else {
        select_38([b, c, d, a, e, f])
    }
}
/// n = 7, i = 2, b < f, b < g, c < d, c < e, c < f, c < g
fn select_740([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_316([e, d, b, f, g, a])
    } else {
        select_739([a, b, c, e, f, g, d])
    }
}
/// n = 9, i = 2, b < i, c < d, c < e, c < f, c < i, f < g, f < h
fn select_741([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < b {
        select_565([a, d, e, f, b, g, h])
    } else {
        select_740([a, b, c, d, e, f, i])
    }
}
/// n = 10, i = 2, c < d, c < e, c < f, c < g, f < j, g < h, g < i
fn select_742([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_738([b, d, e, f, g, h, i, a, j])
    } else {
        select_741([b, a, c, d, e, g, h, i, f])
    }
}
/// n = 7, i = 3, b < f, b < g, c < e, c < g, d < e, d < f, d < g
fn select_743([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if b < c {
        select_260([a, c, d, f, e, g])
    } else {
        select_260([a, b, d, e, f, g])
    }
}
/// n = 10, i = 3, b < f, c < e, c < g, d < e, d < f, d < g, g < h, g < i, g < j
fn select_744([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < b {
        select_541([a, e, g, b, h, i, j])
    } else {
        select_743([a, b, c, d, e, f, g])
    }
}
/// n = 11, i = 3, c < f, c < g, c < k, d < e, d < f, d < g, e < k, g < h, g < i, g < j
fn select_745([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_543([b, e, c, f, a, g, h, i, j, k])
    } else {
        select_744([b, a, c, d, f, e, g, h, i, j])
    }
}
/// n = 12, i = 3, c < e, c < i, d < f, d < i, d < l, e < l, f < g, f < h, f < j, j < k
fn select_746([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < c {
        select_742([a, b, f, g, h, j, c, e, i, k])
    } else {
        select_745([a, b, d, c, e, i, f, g, h, j, l])
    }
}
/// n = 11, i = 3, a < c, a < d, b < e, b < k, d < k, e < f, e < g, e < h, h < i, h < j
fn select_747([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < a {
        select_212([f, g, h, a, i, j])
    } else {
        select_607([a, b, c, d, e, f, g, h, k])
    }
}
/// n = 12, i = 3, a < c, a < d, b < e, b < l, d < l, e < f, e < g, e < h, e < i, h < k, i < j
fn select_748([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < i {
        select_747([a, b, c, d, e, f, g, h, i, k, l])
    } else {
        select_747([a, b, c, d, e, f, g, i, h, j, l])
    }
}
/// n = 9, i = 3, a < c, a < h, a < i, b < d, b < h, c < g, d < e, d < f, d < i
fn select_749([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < c {
        select_176([a, d, e, f, h, i])
    } else {
        select_51([b, a, c, d, f, g, h, i])
    }
}
/// n = 11, i = 3, a < c, a < h, b < d, b < h, c < g, d < e, d < f, d < i, i < j, i < k
fn select_750([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if i < a {
        select_212([e, f, i, a, j, k])
    } else {
        select_749([a, b, c, d, e, f, g, h, i])
    }
}
/// n = 12, i = 3, a < c, a < h, b < d, b < h, c < g, d < e, d < f, d < i, d < j, i < l, j < k
fn select_751([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if i < j {
        select_750([a, b, c, d, e, f, g, h, i, j, l])
    } else {
        select_750([a, b, c, d, e, f, g, h, j, i, k])
    }
}
/// n = 12, i = 3, a < h, b < d, c < e, c < h, e < f, e < g, e < i, e < j, i < l, j < k
fn select_752([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if b < a {
        select_748([b, c, d, a, e, f, g, i, j, k, l, h])
    } else {
        select_751([a, c, b, e, f, g, d, h, i, j, k, l])
    }
}
/// n = 12, i = 3, c < h, d < e, d < h, e < f, e < g, e < i, e < j, i < l, j < k
fn select_753([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_752([c, a, d, b, e, f, g, h, i, j, k, l])
    } else {
        select_752([c, b, d, a, e, f, g, h, i, j, k, l])
    }
}
/// n = 14, i = 3, c < e, c < i, d < f, d < i, d < n, e < n, f < g, f < h, f < j, f < k, j < m, k < l
fn select_754([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if e < j {
        select_746([a, b, c, d, e, f, g, h, i, k, l, n])
    } else {
        select_753([a, b, c, d, f, g, h, i, j, k, l, m])
    }
}
/// n = 9, i = 2, a < e, a < i, b < c, b < d, b < f, b < i, f < g, f < h
fn select_755([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_212([c, d, f, a, g, h])
    } else {
        select_482([a, b, c, d, e, f, i])
    }
}
/// n = 10, i = 2, a < e, a < j, b < c, b < d, b < f, b < g, b < j, f < i, g < h
fn select_756([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < g {
        select_755([a, b, c, d, e, f, g, i, j])
    } else {
        select_755([a, b, c, d, e, g, f, h, j])
    }
}
/// n = 12, i = 2, a < e, b < c, b < d, b < f, b < g, b < h, f < l, g < k, h < i, h < j
fn select_757([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < a {
        select_463([c, d, f, g, h, a, i, j, k, l])
    } else {
        select_756([a, b, c, d, e, f, g, k, l, h])
    }
}
/// n = 10, i = 1, a < g, a < h, a < i, a < j, b < c, b < d, b < e, b < f
fn select_758([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_22([b, g, h, i, j])
    } else {
        select_22([a, c, d, e, f])
    }
}
/// n = 11, i = 1, a < k, b < h, b < i, b < j, c < d, c < e, c < f, c < g
fn select_759([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_155([a, c, d, e, f, g, b, k])
    } else {
        select_758([b, c, d, e, f, g, a, h, i, j])
    }
}
/// n = 13, i = 4, a < e, a < m, b < g, b < l, b < m, c < f, c < g, c < m, d < f, d < g, d < m, f < l, g < h, g < i, g < j, g < k
fn select_760([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if g < e {
        select_504([a, f, b, g, h, i, j, k, l, m])
    } else {
        select_450([b, a, c, d, e, f, l, m])
    }
}
/// n = 15, i = 4, a < e, b < g, b < h, b < o, c < f, c < g, c < h, d < f, d < g, d < h, f < o, g < m, g < n, h < i, h < j, h < k, h < l
fn select_761([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < a {
        select_759([f, g, h, i, j, k, l, a, m, n, o])
    } else {
        select_760([a, b, c, d, e, f, h, i, j, k, l, o, g])
    }
}
/// n = 17, i = 4, a < e, b < f, b < l, c < g, c < l, c < q, d < f, d < g, d < l, f < q, g < h, g < i, g < j, g < k, j < n, k < m, l < o, l < p
fn select_762([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if g < b {
        select_757([a, g, h, i, e, j, k, b, f, l, m, n])
    } else {
        select_761([a, c, b, d, e, f, l, g, h, i, j, k, o, p, q])
    }
}
/// n = 17, i = 4, c < f, c < l, d < g, d < l, d < q, e < f, e < g, e < l, f < q, g < h, g < i, g < j, g < k, j < n, k < m, l < o, l < p
fn select_763([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if a < b {
        select_762([a, c, d, e, b, f, g, h, i, j, k, l, m, n, o, p, q])
    } else {
        select_762([b, c, d, e, a, f, g, h, i, j, k, l, m, n, o, p, q])
    }
}
/// n = 17, i = 4, c < m, d < g, d < j, d < m, e < f, e < g, e < m, f < j, g < h, g < i, g < k, g < l, k < o, l < n, m < p, m < q
fn select_764([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if f < c {
        select_754([a, b, f, d, c, g, h, i, j, k, l, n, o, m])
    } else {
        select_763([a, b, c, d, e, f, g, h, i, k, l, m, n, o, p, q, j])
    }
}
/// n = 17, i = 4, c < m, d < g, d < h, d < m, e < f, e < h, e < m, h < i, h < j, h < k, h < l, k < o, l < n, m < p, m < q
fn select_765([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if f < g {
        select_764([a, b, c, d, e, f, h, i, j, g, k, l, m, n, o, p, q])
    } else {
        select_764([a, b, c, e, d, g, h, i, j, f, k, l, m, n, o, p, q])
    }
}
/// n = 7, i = 3, a < e, a < g, b < e, b < f, b < g, c < d, c < g, d < f
fn select_766([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_10([a, b, f])
    } else {
        select_19([b, c, d, e, g])
    }
}
/// n = 7, i = 3, a < g, b < f, b < g, c < e, c < f, d < e, d < f, d < g
fn select_767([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if b < a {
        select_766([c, d, b, a, e, g, f])
    } else {
        select_96([c, d, a, b, e, g])
    }
}
/// n = 9, i = 3, b < e, b < i, c < f, c < i, d < e, d < f, d < i, f < g, f < h
fn select_768([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_12([b, c, e, f, a, g, h, i])
    } else {
        select_767([a, c, b, d, e, i, f])
    }
}
/// n = 7, i = 3, a < g, b < f, b < g, c < e, c < g, d < e, d < f
fn select_769([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if b < c {
        select_79([a, c, d, f, e, g])
    } else {
        select_79([a, b, d, e, f, g])
    }
}
/// n = 9, i = 3, b < e, b < f, c < f, c < g, d < e, d < g, g < h, g < i
fn select_770([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < g {
        select_769([a, c, d, b, e, f, g])
    } else {
        select_419([b, c, d, e, f, g, a, h, i])
    }
}
/// n = 11, i = 4, b < g, b < h, b < k, c < f, c < h, d < e, d < h, d < k, e < g, f < k, h < i, h < j
fn select_771([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < e {
        select_768([a, f, b, d, e, h, i, j, k])
    } else {
        select_770([a, e, b, c, f, g, h, i, j])
    }
}
/// n = 11, i = 4, b < g, b < h, c < f, c < h, c < k, d < e, d < h, d < k, g < k, h < i, h < j
fn select_772([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_771([a, c, b, d, e, g, f, h, i, j, k])
    } else {
        select_771([a, d, b, c, f, g, e, h, i, j, k])
    }
}
/// n = 6, i = 3, a < f, b < f, c < e, d < e, d < f
fn select_773([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_96([c, d, a, b, e, f])
    } else {
        select_96([c, d, b, a, e, f])
    }
}
/// n = 7, i = 3, b < g, c < f, c < g, d < e, d < g, e < f
fn select_774([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < e {
        select_773([b, c, a, d, e, g])
    } else {
        select_79([b, c, e, a, f, g])
    }
}
/// n = 8, i = 3, a < f, a < h, b < e, b < f, b < g, c < d, c < e, d < g, d < h
fn select_775([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_90([b, d, e, a, h, g])
    } else {
        select_108([b, a, c, e, f, d, h])
    }
}
/// n = 9, i = 4, a < g, a < i, b < f, b < i, c < d, c < e, e < h, e < i, f < g, f < h
fn select_776([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < f {
        select_773([a, e, d, b, f, i])
    } else {
        select_775([a, f, c, e, d, g, h, i])
    }
}
/// n = 9, i = 4, a < h, a < i, b < e, b < i, c < d, c < f, e < h, f < g, f < i
fn select_777([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < e {
        select_774([d, a, b, f, g, e, i])
    } else {
        select_776([a, b, c, d, f, e, h, g, i])
    }
}
/// n = 9, i = 4, a < f, a < i, b < e, b < i, c < d, c < g, g < h, g < i
fn select_778([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < f {
        select_777([a, b, c, d, e, g, h, f, i])
    } else {
        select_777([b, a, c, d, f, g, h, e, i])
    }
}
/// n = 8, i = 3, a < e, a < h, b < e, b < f, b < h, c < d, c < f, c < h, f < g
fn select_779([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < d {
        select_242([a, c, e, f, d, g, h])
    } else {
        select_766([a, b, c, d, e, f, h])
    }
}
/// n = 10, i = 4, a < e, a < i, b < f, b < h, b < i, c < d, c < f, c < i, e < h, f < g, i < j
fn select_780([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_397([d, f, a, g, i, j, e])
    } else {
        select_779([e, b, c, d, h, i, j, f])
    }
}
/// n = 10, i = 4, a < h, a < i, b < f, b < i, c < d, c < e, c < i, e < g, f < h, i < j
fn select_781([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_106([d, b, e, g, f, a, i])
    } else {
        select_780([b, a, c, d, f, e, g, h, i, j])
    }
}
/// n = 10, i = 3, a < d, a < g, b < c, b < g, b < j, c < f, d < e, d < j, g < h, g < i
fn select_782([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < d {
        select_418([c, a, f, g, d, h, i])
    } else {
        select_238([a, b, c, d, e, f, g, j])
    }
}
/// n = 8, i = 3, a < d, b < c, b < h, c < e, c < f, d < g, d < h
fn select_783([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < c {
        select_11([g, b, c, h])
    } else {
        select_73([e, f, a, d])
    }
}
/// n = 10, i = 4, a < d, a < i, b < f, b < g, b < i, b < j, c < e, c < j, d < f, d < j, e < g, e < i, g < h
fn select_784([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_19([b, c, e, f, j])
    } else {
        select_90([a, b, d, g, h, i])
    }
}
/// n = 10, i = 4, a < e, a < j, b < f, b < h, b < i, b < j, c < d, c < f, c < i, d < j, e < h, e < i, f < g
fn select_785([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < d {
        select_783([a, c, f, e, d, g, h, i])
    } else {
        select_784([a, b, c, e, d, h, f, g, j, i])
    }
}
/// n = 11, i = 4, a < e, a < i, b < f, b < h, b < i, b < k, c < d, c < f, c < i, c < k, e < h, e < k, f < g, i < j
fn select_786([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if i < d {
        select_782([a, c, f, e, h, g, i, d, j, k])
    } else {
        select_785([a, b, c, d, e, f, g, h, k, i])
    }
}
/// n = 11, i = 4, a < h, a < i, a < k, b < f, b < i, c < d, c < e, c < i, c < k, e < g, f < h, f < k, i < j
fn select_787([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_106([d, b, e, g, f, a, i])
    } else {
        select_786([b, a, c, d, f, e, g, h, i, j, k])
    }
}
/// n = 11, i = 4, a < g, a < i, b < e, b < i, b < k, c < d, c < f, c < i, c < k, f < h, g < k, i < j
fn select_788([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < g {
        select_781([a, b, c, d, f, e, h, g, i, j])
    } else {
        select_787([b, a, c, d, f, g, h, e, i, j, k])
    }
}
/// n = 11, i = 4, a < g, b < h, b < i, c < f, c < i, c < k, d < e, d < i, d < k, h < k, i < j
fn select_789([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < c {
        select_778([b, d, a, g, e, h, c, f, i])
    } else {
        select_788([b, d, c, f, e, a, h, g, i, j, k])
    }
}
/// n = 10, i = 5, a < h, a < j, b < f, b < i, c < f, c < i, d < e, d < j, e < h, e < i, f < g, f < j
fn select_790([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_74([a, b, c, h, i, f, g])
    } else {
        select_256([g, a, d, e, i, j])
    }
}
/// n = 7, i = 3, a < g, b < f, c < f, c < g, d < e, d < g
fn select_791([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_93([c, d, a, e, b, f, g])
    } else {
        select_105([c, d, b, a, e, f])
    }
}
/// n = 10, i = 5, a < i, a < j, b < e, b < j, c < f, c < g, d < f, d < g, e < i, g < h, g < j
fn select_792([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_790([a, c, d, b, e, g, h, i, f, j])
    } else {
        select_791([a, f, b, g, h, e, j])
    }
}
/// n = 10, i = 5, a < f, a < j, b < e, b < j, c < g, c < h, d < g, d < h, h < i, h < j
fn select_793([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_792([a, b, c, d, e, g, h, i, f, j])
    } else {
        select_792([b, a, c, d, f, g, h, i, e, j])
    }
}
/// n = 12, i = 5, a < i, b < f, b < j, c < e, c < j, c < l, d < g, d < i, f < l, g < h, g < j, g < l, j < k
fn select_794([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < g {
        select_793([b, c, a, d, e, f, i, g, h, j])
    } else {
        select_788([b, c, g, h, e, a, f, i, j, k, l])
    }
}
/// n = 12, i = 5, b < g, b < j, c < f, c < j, c < l, d < e, d < h, g < l, h < i, h < j, h < l, j < k
fn select_795([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < a {
        select_789([e, b, c, h, i, f, a, g, j, k, l])
    } else {
        select_794([a, b, c, d, f, g, h, i, e, j, k, l])
    }
}
/// n = 13, i = 5, b < g, b < j, c < f, c < j, c < m, d < e, d < h, g < m, h < i, h < j, h < m, j < k, j < l
fn select_796([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if k < a {
        select_772([e, b, c, h, i, f, g, j, k, l, m])
    } else {
        select_795([a, b, c, d, e, f, g, h, i, j, l, m])
    }
}
/// n = 5, i = 3, b < e, c < e, d < e
fn select_797([a, b, c, d, e]: [usize; 5]) -> usize {
    if b < a {
        select_44([a, c, d, e])
    } else {
        select_70([b, c, d])
    }
}
/// n = 7, i = 4, a < g, b < e, c < f, d < f, f < g
fn select_798([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if f < e {
        select_92([a, b, f, e, g])
    } else {
        select_797([a, c, d, e, f])
    }
}
/// n = 7, i = 4, b < g, c < e, d < f, f < g
fn select_799([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < f {
        select_798([b, c, a, d, e, f, g])
    } else {
        select_105([b, c, f, a, e, g])
    }
}
/// n = 6, i = 3, b < f, c < e, c < f, d < e, d < f
fn select_800([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if b < a {
        select_45([c, d, b, a, e, f])
    } else {
        select_71([c, d, a, b, e])
    }
}
/// n = 9, i = 3, b < e, c < f, d < e, d < f, f < g, f < h, f < i
fn select_801([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < b {
        select_49([a, f, b, g, h, i])
    } else {
        select_800([a, c, b, d, e, f])
    }
}
/// n = 11, i = 4, a < e, b < h, c < g, c < h, d < f, d < h, f < g, h < i, h < j, h < k
fn select_802([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < h {
        select_799([b, c, a, d, e, f, g])
    } else {
        select_801([a, f, b, c, g, h, i, j, k])
    }
}
/// n = 11, i = 4, c < h, d < g, d < h, e < f, e < h, f < g, h < i, h < j, h < k
fn select_803([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_802([a, c, d, e, b, f, g, h, i, j, k])
    } else {
        select_802([b, c, d, e, a, f, g, h, i, j, k])
    }
}
/// n = 11, i = 4, c < h, d < g, d < h, e < f, e < h, h < i, h < j, h < k
fn select_804([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < g {
        select_803([a, b, c, d, e, f, g, h, i, j, k])
    } else {
        select_803([a, b, c, e, d, g, f, h, i, j, k])
    }
}
/// n = 14, i = 5, b < g, b < j, c < f, c < j, c < n, d < e, d < h, g < n, h < i, h < j, h < n, j < k, j < l, j < m
fn select_805([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if k < g {
        select_804([a, e, b, c, h, i, f, j, k, l, m])
    } else {
        select_796([a, b, c, d, e, f, g, h, i, j, l, m, n])
    }
}
/// n = 16, i = 5, b < j, c < k, d < g, d < j, d < k, e < f, e < h, h < i, h < j, h < k, j < o, j < p, k < l, k < m, k < n
fn select_806([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if b < c {
        select_796([a, b, d, e, f, g, c, h, i, j, o, p, k])
    } else {
        select_805([a, c, d, e, f, g, b, h, i, k, l, m, n, j])
    }
}
/// n = 18, i = 5, c < n, d < g, d < j, d < n, e < f, e < h, h < i, h < j, h < n, j < k, j < l, j < m, l < p, m < o, n < q, n < r
fn select_807([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if j < a {
        select_765([b, f, c, d, h, i, g, j, a, k, l, m, n, o, p, q, r])
    } else {
        select_806([b, c, a, d, e, f, g, h, i, n, j, k, l, m, q, r])
    }
}
/// n = 18, i = 5, d < g, d < j, d < k, e < f, e < h, h < i, h < j, h < k, j < m, j < n, k < l, k < o, k < p, o < r, p < q
fn select_808([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if j < a {
        select_737([b, c, f, d, h, i, g, j, k, l, a, m, n, o, p, q, r])
    } else {
        select_807([b, c, a, d, e, f, g, h, i, k, l, o, p, j, q, r, m, n])
    }
}
/// n = 18, i = 5, d < g, d < n, e < f, e < h, h < i, h < j, h < n, j < k, j < l, j < m, l < p, m < o, n < q, n < r
fn select_809([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if j < d {
        select_719([a, b, c, f, h, i, j, k, l, m, d, g, o, p, n, q, r])
    } else {
        select_808([a, b, c, d, e, f, g, h, i, n, j, k, q, r, l, m, o, p])
    }
}
/// n = 18, i = 5, d < g, e < f, e < h, h < i, h < j, h < k, j < m, j < n, k < l, k < o, k < p, o < r, p < q
fn select_810([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if j < d {
        select_563([a, b, c, f, h, i, j, k, l, m, n, o, p, d, q, r, g])
    } else {
        select_809([a, b, c, d, e, f, g, h, i, k, l, o, p, j, q, r, m, n])
    }
}
/// n = 18, i = 5, f < g, f < h, h < i, h < j, h < k, j < m, j < n, k < l, k < o, k < p, o < r, p < q
fn select_811([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_810([c, d, e, a, f, g, b, h, i, j, k, l, m, n, o, p, q, r])
    } else {
        select_810([c, d, e, b, f, g, a, h, i, j, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, g < h, g < i, i < j, i < k, i < l, k < n, l < m, l < o, l < p, o < r, p < q
fn select_812([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < k {
        select_462([b, c, d, e, f, a, g, h, i, j, l, m, o, p, k, q, r, n])
    } else {
        select_811([b, c, d, e, f, g, h, i, j, k, l, m, a, n, o, p, q, r])
    }
}
/// n = 8, i = 3, a < d, a < g, b < c, b < g, c < e, d < f, g < h
fn select_813([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_90([c, a, e, g, h, d])
    } else {
        select_90([d, b, f, g, h, c])
    }
}
/// n = 10, i = 3, a < c, a < h, b < d, b < h, c < f, d < e, d < g, g < i, h < j
fn select_814([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < c {
        select_694([a, d, e, g, h, i, j])
    } else {
        select_813([a, b, d, c, e, f, h, j])
    }
}
/// n = 11, i = 3, a < c, a < h, a < k, b < d, b < h, c < f, d < e, d < g, d < k, g < i, h < j
fn select_815([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < c {
        select_575([a, d, e, g, h, i, j, k])
    } else {
        select_332([b, a, c, d, e, f, h, j, k])
    }
}
/// n = 11, i = 3, a < d, a < i, a < k, b < c, b < e, b < i, c < g, d < h, e < f, e < k, i < j
fn select_816([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < e {
        select_814([a, b, d, c, g, h, e, i, f, j])
    } else {
        select_815([a, b, d, e, f, h, c, i, g, j, k])
    }
}
/// n = 10, i = 3, a < f, a < g, b < d, b < e, b < g, c < d, c < e, c < f, e < h, f < i, g < j
fn select_817([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_11([d, e, a, h])
    } else {
        select_167([b, c, a, d, f, g, i, j, e])
    }
}
/// n = 10, i = 3, a < f, a < h, b < d, b < g, c < f, c < g, c < h, d < e, g < i, h < j
fn select_818([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_85([c, d, a, e, g, i])
    } else {
        select_817([b, a, c, f, h, g, d, j, i, e])
    }
}
/// n = 11, i = 3, a < h, b < d, b < i, b < k, c < e, c < h, c < i, d < g, e < f, e < k, i < j
fn select_819([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < e {
        select_818([a, b, c, d, g, h, i, e, j, f])
    } else {
        select_815([b, c, d, e, f, g, a, i, h, j, k])
    }
}
/// n = 11, i = 3, b < e, b < i, b < k, c < d, c < f, c < i, e < h, f < g, f < k, i < j
fn select_820([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_816([b, c, d, e, f, g, a, h, i, j, k])
    } else {
        select_819([a, b, c, e, f, g, h, d, i, j, k])
    }
}
/// n = 12, i = 3, b < f, b < j, c < e, c < i, d < g, d < i, d < j, g < h, i < k, j < l
fn select_821([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if b < c {
        select_820([a, d, b, f, g, c, e, h, j, l, i])
    } else {
        select_820([a, d, c, e, g, b, f, h, i, k, j])
    }
}
/// n = 10, i = 3, a < f, a < h, b < e, b < g, c < d, c < g, c < h, g < i, h < j
fn select_822([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_82([f, b, c, d, e, h, j, g])
    } else {
        select_82([e, a, c, d, f, g, i, h])
    }
}
/// n = 9, i = 2, c < d, c < e, d < i, e < f, e < g, e < h
fn select_823([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_146([b, d, e, f, g, h, a, i])
    } else {
        select_606([b, a, c, e, f, g, h, d])
    }
}
/// n = 11, i = 3, b < d, b < h, b < k, c < e, c < h, e < f, e < g, e < k, g < i, h < j
fn select_824([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < b {
        select_566([a, f, g, b, d, h, k, i])
    } else {
        select_823([a, d, c, h, e, f, g, k, j])
    }
}
/// n = 12, i = 4, a < c, a < e, a < j, b < d, b < f, d < h, e < i, e < l, f < g, f < j, f < l, j < k
fn select_825([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < e {
        select_822([d, f, a, c, g, h, j, e, k, i])
    } else {
        select_824([c, e, b, i, f, g, j, d, k, h, l])
    }
}
/// n = 9, i = 3, a < d, b < f, b < i, c < e, c < f, e < i, f < g, f < h
fn select_826([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_24([e, f, a, g, h, i])
    } else {
        select_93([b, a, c, d, e, i, f])
    }
}
/// n = 9, i = 3, a < f, b < e, b < g, c < d, c < g, g < h, g < i
fn select_827([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_826([a, b, c, f, d, g, h, i, e])
    } else {
        select_826([a, c, b, f, e, g, h, i, d])
    }
}
/// n = 8, i = 3, a < e, a < h, b < d, b < h, c < e, c < g, c < h, d < g, e < f
fn select_828([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < d {
        select_72([b, e, f, h])
    } else {
        select_92([a, d, c, g, h])
    }
}
/// n = 9, i = 3, a < f, a < i, b < d, b < e, b < i, c < e, c < f, c < i, e < g, f < h
fn select_829([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < d {
        select_134([a, b, f, e, d, g, h, i])
    } else {
        select_828([a, b, c, d, f, h, e, i])
    }
}
/// n = 10, i = 3, a < j, b < d, b < g, b < i, b < j, c < e, c < g, c < j, e < f, e < i, g < h
fn select_830([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_601([e, b, d, a, f, g, h, i])
    } else {
        select_829([a, b, c, d, g, e, h, f, j])
    }
}
/// n = 11, i = 3, b < d, b < g, b < h, b < k, c < e, c < g, c < h, e < f, e < k, g < j, h < i
fn select_831([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_154([e, b, d, f, h, g, a, j, i, k])
    } else {
        select_830([a, b, c, d, e, f, h, i, k, g])
    }
}
/// n = 12, i = 4, a < c, a < f, b < d, b < e, b < j, d < h, e < g, e < l, f < i, f < j, f < l, j < k
fn select_832([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < f {
        select_827([e, a, d, h, c, g, f, i, j])
    } else {
        select_831([c, f, b, i, e, g, d, j, k, h, l])
    }
}
/// n = 14, i = 4, a < c, a < f, a < k, b < d, b < e, b < j, d < h, e < g, e < k, e < n, f < i, f < j, f < n, j < l, k < m
fn select_833([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if k < j {
        select_825([a, b, c, d, f, e, g, h, i, k, m, n])
    } else {
        select_832([a, b, c, d, e, f, g, h, i, j, l, n])
    }
}
/// n = 14, i = 4, a < e, a < f, a < l, b < c, b < d, b < g, d < i, e < k, f < j, f < n, g < h, g < l, g < n, l < m
fn select_834([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if d < f {
        select_821([c, d, g, a, h, i, e, k, l, f, m, j])
    } else {
        select_833([b, a, c, e, f, g, j, k, h, l, d, m, i, n])
    }
}
/// n = 9, i = 2, a < e, a < i, b < f, b < h, c < d, c < h, c < i, f < g
fn select_835([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_39([c, a, e, d, b, f, i])
    } else {
        select_574([c, b, d, a, f, g, e, h])
    }
}
/// n = 10, i = 2, a < d, a < j, b < c, b < e, b < j, d < i, e < f, e < g, e < h
fn select_836([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_49([c, e, a, f, g, h])
    } else {
        select_150([b, a, c, d, i, e, j])
    }
}
/// n = 11, i = 2, a < e, b < f, b < k, c < d, c < g, c < k, f < j, g < h, g < i
fn select_837([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < g {
        select_835([a, b, c, d, e, f, j, k, g])
    } else {
        select_836([b, c, d, f, g, a, h, i, j, k])
    }
}
/// n = 13, i = 2, a < e, b < f, c < d, c < g, c < h, f < m, g < k, g < l, h < i, h < j
fn select_838([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if b < g {
        select_837([a, b, c, d, e, f, h, i, j, m, g])
    } else {
        select_656([a, c, d, e, h, g, b, k, l, i, j])
    }
}
/// n = 6, i = 2, b < f, c < d, c < e, c < f
fn select_839([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < a {
        select_42([e, b, d, a, f])
    } else {
        select_80([a, b, c, e, f, d])
    }
}
/// n = 8, i = 3, a < d, a < h, b < c, b < e, d < g, e < f, e < h
fn select_840([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_79([c, a, e, f, h, d])
    } else {
        select_235([a, b, e, d, f, g, c, h])
    }
}
/// n = 9, i = 3, a < d, a < i, b < c, b < e, d < h, e < f, e < g, e < i
fn select_841([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < d {
        select_839([c, a, e, f, g, i])
    } else {
        select_840([a, b, c, d, e, g, h, i])
    }
}
/// n = 10, i = 3, a < d, a < e, b < e, b < f, c < d, c < f, d < i, e < j, f < g, f < h
fn select_842([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_3([a, g, h])
    } else {
        select_137([b, c, d, e, i, j, f])
    }
}
/// n = 10, i = 3, a < g, a < i, b < f, b < g, c < d, c < f, d < e, d < i, f < h, g < j
fn select_843([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_694([b, d, e, a, f, i, h])
    } else {
        select_842([b, a, c, f, g, d, e, i, h, j])
    }
}
/// n = 10, i = 3, a < d, a < h, b < g, b < h, c < e, c < g, e < f, g < i, h < j
fn select_844([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_516([c, b, a, d, h, g, j, i, e])
    } else {
        select_843([a, b, c, e, f, g, h, i, d, j])
    }
}
/// n = 11, i = 3, a < i, b < d, b < f, c < e, c < i, c < j, e < g, f < h, f < j, i < k
fn select_845([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_841([c, b, d, e, f, a, h, g, j])
    } else {
        select_844([b, a, c, d, e, g, i, f, k, h])
    }
}
/// n = 9, i = 3, a < d, a < i, b < g, b < i, c < e, c < g, c < i, e < f, g < h
fn select_846([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_694([b, e, f, a, g, d, h])
    } else {
        select_829([b, a, c, d, e, g, f, h, i])
    }
}
/// n = 12, i = 3, a < g, b < d, b < h, c < e, c < g, c < h, e < f, g < l, h < i, h < j, h < k
fn select_847([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < a {
        select_470([e, b, d, f, h, a, i, j, k])
    } else {
        select_846([b, a, c, d, e, f, g, l, h])
    }
}
/// n = 13, i = 3, a < i, b < d, b < f, b < j, c < e, c < i, c < j, e < g, f < h, i < m, j < k, j < l
fn select_848([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if f < j {
        select_845([a, b, c, d, e, f, g, h, i, j, m])
    } else {
        select_847([a, b, c, d, e, g, i, j, f, k, l, m])
    }
}
/// n = 15, i = 3, a < k, b < d, b < f, c < e, c < g, c < k, e < i, f < j, g < h, g < l, k < o, l < m, l < n
fn select_849([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < b {
        select_838([e, a, g, h, i, k, b, l, m, n, d, f, o])
    } else {
        select_848([a, b, c, d, e, f, i, j, k, g, h, l, o])
    }
}
/// n = 11, i = 2, a < g, b < e, b < f, b < k, c < d, c < h, c < k, h < i, h < j
fn select_850([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < c {
        select_623([a, b, e, f, g, c, d, h, k])
    } else {
        select_656([a, c, d, g, h, b, e, f, k, i, j])
    }
}
/// n = 11, i = 3, a < d, a < g, a < k, b < c, b < g, b < j, c < e, c < k, d < f, d < j, g < h, g < i
fn select_851([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < d {
        select_152([c, a, e, g, h, i, d, k])
    } else {
        select_152([d, b, f, g, h, i, c, j])
    }
}
/// n = 11, i = 3, a < d, a < h, a < k, b < c, b < e, b < h, d < g, e < f, e < k, h < i, h < j
fn select_852([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < d {
        select_539([c, e, a, f, h, i, j, k, d])
    } else {
        select_851([a, b, e, d, f, g, h, i, j, c, k])
    }
}
/// n = 13, i = 3, a < c, a < e, a < k, b < d, b < f, b < k, d < i, e < j, f < g, f < h, k < l, k < m
fn select_853([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if f < e {
        select_850([d, f, a, c, g, h, i, k, l, m, e])
    } else {
        select_852([b, a, c, d, e, j, i, k, l, m, f])
    }
}
/// n = 8, i = 3, a < e, a < g, a < h, b < e, b < f, b < h, c < d, c < h, d < f, d < g
fn select_854([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < d {
        select_10([e, c, h])
    } else {
        select_78([a, b, d, f, g, h])
    }
}
/// n = 8, i = 3, a < f, a < g, a < h, b < e, b < h, c < d, c < f, c < h, e < g
fn select_855([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_79([d, b, a, f, h, e])
    } else {
        select_854([a, c, b, e, f, d, g, h])
    }
}
/// n = 8, i = 3, a < e, a < h, b < e, b < f, b < g, b < h, c < d, c < h, d < f, d < g
fn select_856([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_11([a, b, f, g])
    } else {
        select_19([b, c, d, e, h])
    }
}
/// n = 10, i = 3, a < e, a < j, b < e, b < f, b < i, b < j, c < d, c < f, c < j, d < i, f < g, f < h
fn select_857([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < d {
        select_12([a, c, e, f, d, g, h, j])
    } else {
        select_856([a, b, c, d, e, f, i, j])
    }
}
/// n = 11, i = 3, a < d, a < f, a < k, b < f, b < g, b < j, b < k, c < e, c < g, c < k, e < j, g < h, g < i
fn select_858([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < g {
        select_855([b, c, a, d, e, f, j, k])
    } else {
        select_857([a, b, c, e, f, g, h, i, j, k])
    }
}
/// n = 13, i = 3, a < d, a < f, b < f, b < g, b < h, b < m, c < e, c < g, c < h, e < m, g < k, g < l, h < i, h < j
fn select_859([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if g < a {
        select_7([e, h, g, a, k, l, i, j, m])
    } else {
        select_858([a, b, c, d, e, f, h, i, j, m, g])
    }
}
/// n = 9, i = 3, a < d, a < g, a < h, a < i, b < c, b < e, b < g, d < f, e < h, e < i
fn select_860([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_739([c, e, a, g, h, i, d])
    } else {
        select_40([d, b, g, f, e, h, i, c])
    }
}
/// n = 9, i = 2, a < c, a < h, a < i, b < d, b < h, b < i, d < e, d < f, d < g
fn select_861([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_4([a, e, f, g])
    } else {
        select_18([c, b, d, h, i])
    }
}
/// n = 11, i = 2, a < c, a < j, a < k, b < d, b < e, b < j, b < k, d < h, d < i, e < f, e < g
fn select_862([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_861([a, b, c, d, e, h, i, j, k])
    } else {
        select_861([a, b, c, e, d, f, g, j, k])
    }
}
/// n = 14, i = 3, a < d, a < g, a < h, a < n, b < c, b < g, b < h, b < m, c < e, c < n, d < f, d < m, g < k, g < l, h < i, h < j
fn select_863([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if c < d {
        select_862([c, a, e, g, h, i, j, k, l, d, n])
    } else {
        select_862([d, b, f, g, h, i, j, k, l, c, m])
    }
}
/// n = 14, i = 3, a < d, a < g, b < h, b < i, b < n, c < e, c < g, c < h, c < i, e < f, e < n, h < l, h < m, i < j, i < k
fn select_864([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if a < b {
        select_860([c, a, d, e, b, f, g, h, i])
    } else {
        select_863([b, c, e, a, f, d, h, i, j, k, l, m, g, n])
    }
}
/// n = 14, i = 3, a < e, a < h, b < d, b < i, b < j, c < f, c < h, c < i, c < j, f < g, i < m, i < n, j < k, j < l
fn select_865([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if d < f {
        select_859([a, c, b, e, d, h, i, j, k, l, m, n, f])
    } else {
        select_864([a, b, c, e, f, g, h, i, j, k, l, m, n, d])
    }
}
/// n = 16, i = 4, a < d, a < j, a < m, a < n, b < c, b < e, b < j, c < h, c < m, d < g, d < i, e < f, e < n, i < k, j < l, n < o, n < p
fn select_866([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if d < e {
        select_853([d, b, g, j, i, c, h, m, l, k, e, f, n])
    } else {
        select_865([c, e, a, f, h, j, l, m, d, n, o, p, g, i])
    }
}
/// n = 16, i = 4, a < d, a < f, a < k, b < c, b < e, b < k, b < n, d < i, e < g, e < j, f < h, f < n, j < l, k < m, n < o, n < p
fn select_867([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if c < d {
        select_849([c, e, a, g, k, j, f, h, m, l, d, n, o, p, i])
    } else {
        select_866([b, a, d, e, f, h, g, i, j, k, l, m, c, n, o, p])
    }
}
/// n = 16, i = 4, a < e, a < g, b < d, b < l, b < n, c < f, c < h, c < l, f < j, g < k, h < i, h < n, l < m, n < o, n < p
fn select_868([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_834([c, a, e, g, f, h, b, d, k, i, j, l, m, n])
    } else {
        select_867([c, b, d, f, a, h, e, i, j, g, l, k, m, n, o, p])
    }
}
/// n = 7, i = 2, a < e, b < f, b < g, c < d, c < f, c < g
fn select_869([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_107([c, a, b, e, d])
    } else {
        select_150([c, b, d, a, e, f, g])
    }
}
/// n = 8, i = 3, a < f, b < d, b < g, b < h, c < e, c < f, e < g, e < h
fn select_870([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_400([b, a, c, d, e, f])
    } else {
        select_150([b, e, d, a, f, g, h])
    }
}
/// n = 8, i = 3, b < e, b < g, b < h, c < d, c < f, f < g, f < h
fn select_871([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_869([d, f, b, e, a, g, h])
    } else {
        select_870([a, b, c, e, f, d, g, h])
    }
}
/// n = 8, i = 3, a < d, a < f, b < d, b < e, c < e, c < f, e < g, f < h
fn select_872([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_84([a, c, d, e, g])
    } else {
        select_84([b, c, d, f, h])
    }
}
/// n = 9, i = 3, a < f, b < f, b < g, b < i, c < d, c < g, d < e, d < i, g < h
fn select_873([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_423([b, d, a, e, g, h, i])
    } else {
        select_872([a, b, c, f, g, d, h, e])
    }
}
/// n = 10, i = 3, a < d, a < g, a < j, b < c, b < g, b < i, c < e, c < j, d < f, d < i, g < h
fn select_874([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_150([c, a, e, g, h, d, j])
    } else {
        select_150([d, b, f, g, h, c, i])
    }
}
/// n = 10, i = 3, b < d, b < g, b < i, c < e, c < g, c < j, d < j, e < f, e < i, g < h
fn select_875([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < d {
        select_873([a, b, c, e, f, d, g, h, i])
    } else {
        select_874([b, c, e, d, f, a, g, h, j, i])
    }
}
/// n = 10, i = 3, b < e, b < j, c < g, c < i, c < j, d < f, d < g, d < j, f < i, g < h
fn select_876([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < c {
        select_871([a, d, b, e, f, c, g, j])
    } else {
        select_875([a, d, c, f, b, e, g, h, j, i])
    }
}
/// n = 9, i = 4, a < f, a < h, a < i, b < e, b < g, c < d, c < g, g < h, g < i
fn select_877([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_870([d, a, b, f, g, e, h, i])
    } else {
        select_870([e, a, c, f, g, d, h, i])
    }
}
/// n = 11, i = 4, a < e, a < k, b < f, b < h, b < k, c < d, c < g, f < j, g < h, g < j, g < k, h < i
fn select_878([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_875([d, b, g, f, a, e, h, i, k, j])
    } else {
        select_877([b, a, c, d, e, f, g, h, k])
    }
}
/// n = 11, i = 4, a < f, a < k, b < e, b < i, b < k, c < d, c < g, g < h, g < i, g < k, i < j
fn select_879([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < e {
        select_876([d, a, b, g, f, h, i, j, e, k])
    } else {
        select_878([a, b, c, d, f, e, g, i, j, h, k])
    }
}
/// n = 9, i = 3, a < e, a < f, b < d, b < f, c < d, c < e, d < g, e < h, f < i
fn select_880([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_300([a, c, d, f, g, i])
    } else {
        select_300([b, c, e, f, h, i])
    }
}
/// n = 10, i = 3, a < f, a < j, b < e, b < f, b < h, c < d, c < e, d < h, d < j, e < g, f < i
fn select_881([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_137([b, d, a, e, j, g, h])
    } else {
        select_880([a, b, c, e, d, f, g, j, i])
    }
}
/// n = 10, i = 3, a < d, a < g, b < e, b < f, c < f, c < g, c < i, e < i, f < h, g < j
fn select_882([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_516([b, c, a, d, g, f, j, h, e])
    } else {
        select_881([a, c, b, e, f, g, h, i, j, d])
    }
}
/// n = 11, i = 3, a < h, b < g, c < e, c < f, d < f, d < g, d < h, f < i, g < j, h < k
fn select_883([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_882([c, a, d, e, b, h, f, k, g, i])
    } else {
        select_882([c, b, d, e, a, g, f, j, h, i])
    }
}
/// n = 9, i = 2, a < e, b < c, b < d, b < f, e < i, f < g, f < h
fn select_884([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_212([c, d, f, a, g, h])
    } else {
        select_423([a, b, c, d, e, i, f])
    }
}
/// n = 11, i = 3, a < f, b < d, b < e, b < g, c < e, c < f, c < g, e < j, f < k, g < h, g < i
fn select_885([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_149([d, e, g, a, h, i, j])
    } else {
        select_829([a, b, c, d, e, f, j, k, g])
    }
}
/// n = 11, i = 3, a < i, b < d, b < h, c < e, c < h, c < i, e < f, e < g, h < j, i < k
fn select_886([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < b {
        select_884([a, e, f, g, i, b, d, h, k])
    } else {
        select_885([a, b, c, d, h, i, e, f, g, j, k])
    }
}
/// n = 11, i = 3, b < i, c < e, c < h, d < f, d < h, d < i, f < g, h < j, i < k
fn select_887([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < f {
        select_883([a, b, c, d, e, h, i, f, j, k, g])
    } else {
        select_886([b, c, d, e, f, a, g, h, i, j, k])
    }
}
/// n = 8, i = 2, a < e, b < c, b < d, c < g, d < f, e < h
fn select_888([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < a {
        select_27([d, c, a, g, f])
    } else {
        select_137([a, b, d, e, f, h, c])
    }
}
/// n = 10, i = 3, a < d, a < g, b < e, b < f, c < e, c < f, c < g, e < i, f < h, g < j
fn select_889([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < d {
        select_888([a, b, e, f, g, h, i, j])
    } else {
        select_312([b, a, c, d, g, f, j, h])
    }
}
/// n = 10, i = 3, a < h, b < d, b < g, c < e, c < g, c < h, e < f, g < i, h < j
fn select_890([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_693([b, e, f, d, a, g, h, i])
    } else {
        select_889([b, a, c, d, e, h, g, j, f, i])
    }
}
/// n = 8, i = 3, a < f, a < h, b < d, b < g, c < e, c < f, e < g, e < h
fn select_891([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < a {
        select_256([d, a, c, e, g, f])
    } else {
        select_62([b, c, f, d, e, h])
    }
}
/// n = 9, i = 4, a < e, a < i, b < f, b < g, c < d, c < g, f < h, g < h, g < i
fn select_892([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < f {
        select_401([d, a, b, e, g, f, i])
    } else {
        select_891([f, a, c, e, g, d, i, h])
    }
}
/// n = 11, i = 4, a < e, b < d, b < i, c < f, c < g, f < h, g < h, g < i, h < j, i < k
fn select_893([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_890([f, b, g, d, a, e, i, h, k, j])
    } else {
        select_892([b, c, a, e, d, f, g, h, i])
    }
}
/// n = 9, i = 2, a < e, a < g, b < c, b < d, b < f, f < h, g < i
fn select_894([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_173([c, d, f, a, h])
    } else {
        select_601([b, a, e, c, d, g, i, f])
    }
}
/// n = 6, i = 4, a < f, b < e, c < d
fn select_895([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if d < e {
        select_71([b, d, a, f, e])
    } else {
        select_71([c, e, a, f, d])
    }
}
/// n = 8, i = 4, a < e, b < f, c < d, c < g, f < g, g < h
fn select_896([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if g < e {
        select_550([a, d, f, g, h])
    } else {
        select_895([a, b, c, d, f, e])
    }
}
/// n = 9, i = 3, a < e, b < d, b < f, c < e, c < f, e < i, f < g, f < h
fn select_897([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_18([d, f, a, g, h])
    } else {
        select_248([b, a, c, d, e, i, f])
    }
}
/// n = 11, i = 4, a < e, a < g, b < d, b < h, c < f, f < g, f < h, g < k, h < i, h < j
fn select_898([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < h {
        select_896([b, c, a, e, d, f, g, k])
    } else {
        select_897([a, b, f, d, g, h, i, j, k])
    }
}
/// n = 11, i = 4, a < e, b < d, b < j, c < f, f < g, f < j, g < h, g < i, j < k
fn select_899([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_894([b, g, h, i, d, a, j, e, k])
    } else {
        select_898([b, a, c, e, d, f, j, g, h, i, k])
    }
}
/// n = 11, i = 4, a < f, b < e, b < j, c < d, c < g, g < h, g < j, h < i, j < k
fn select_900([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < h {
        select_893([a, b, c, e, f, d, g, h, j, i, k])
    } else {
        select_899([a, b, c, e, f, g, h, d, i, j, k])
    }
}
/// n = 13, i = 4, a < f, a < k, b < e, b < j, c < d, c < g, g < h, g < j, g < k, h < i, j < l, k < m
fn select_901([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if k < e {
        select_887([d, b, a, g, f, h, i, k, j, m, l])
    } else {
        select_900([a, b, c, d, e, f, g, h, i, j, l])
    }
}
/// n = 14, i = 4, a < f, a < l, a < n, b < e, b < g, c < d, c < h, c < n, g < i, g < n, h < j, h < l, j < k, l < m
fn select_902([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if g < h {
        select_879([a, c, b, e, d, f, g, i, h, j, n])
    } else {
        select_901([a, b, c, d, e, f, h, j, k, g, l, i, m])
    }
}
/// n = 7, i = 4, a < f, b < e, b < g, c < d, c < g, f < g
fn select_903([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < e {
        select_96([d, b, a, f, e, g])
    } else {
        select_96([e, c, a, f, d, g])
    }
}
/// n = 10, i = 2, a < e, b < i, b < j, c < d, c < f, c < i, c < j, f < g, f < h
fn select_904([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_146([d, b, f, a, g, h, i, j])
    } else {
        select_202([b, a, c, d, e, f, i, j])
    }
}
/// n = 8, i = 2, a < e, b < f, b < g, b < h, c < d, c < f, c < g, c < h
fn select_905([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_107([c, a, b, e, d])
    } else {
        select_25([c, b, d, a, e, f, g, h])
    }
}
/// n = 11, i = 2, a < e, b < j, b < k, c < d, c < f, c < j, c < k, f < g, f < h, f < i
fn select_906([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < f {
        select_905([a, b, c, d, e, f, j, k])
    } else {
        select_470([a, c, d, e, f, b, g, h, i])
    }
}
/// n = 12, i = 2, a < e, b < k, b < l, c < d, c < f, c < g, c < k, c < l, f < j, g < h, g < i
fn select_907([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < g {
        select_904([a, b, c, d, e, f, g, j, k, l])
    } else {
        select_906([a, b, c, d, e, g, f, h, i, k, l])
    }
}
/// n = 12, i = 2, c < k, c < l, d < e, d < f, d < g, d < k, d < l, f < j, g < h, g < i
fn select_908([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_907([a, c, d, e, b, f, g, h, i, j, k, l])
    } else {
        select_907([b, c, d, e, a, f, g, h, i, j, k, l])
    }
}
/// n = 14, i = 4, a < f, a < n, b < e, b < g, c < d, c < g, g < h, g < i, g < j, g < n, i < m, j < k, j < l
fn select_909([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if f < g {
        select_903([a, b, c, d, e, f, g])
    } else {
        select_908([d, e, a, g, h, i, j, k, l, m, f, n])
    }
}
/// n = 9, i = 2, a < d, a < f, a < i, b < c, b < e, b < i, e < g, f < h
fn select_910([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < f {
        select_39([a, b, c, d, e, g, i])
    } else {
        select_39([b, a, d, c, f, h, i])
    }
}
/// n = 10, i = 3, a < e, b < d, b < h, b < j, c < f, c < h, f < g, f < j, h < i
fn select_911([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_910([b, f, g, d, a, h, e, i, j])
    } else {
        select_517([a, b, c, d, e, h, f, i, g])
    }
}
/// n = 10, i = 3, c < e, c < h, c < j, d < f, d < h, f < g, f < j, h < i
fn select_912([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_911([a, c, d, e, b, f, g, h, i, j])
    } else {
        select_911([b, c, d, e, a, f, g, h, i, j])
    }
}
/// n = 12, i = 3, c < e, c < h, c < i, d < f, d < h, d < i, f < g, h < l, i < j, i < k
fn select_913([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < i {
        select_912([a, b, c, d, e, f, g, h, l, i])
    } else {
        select_652([a, b, d, c, e, h, i, f, j, k, l])
    }
}
/// n = 14, i = 4, a < f, b < e, b < j, b < k, c < d, c < g, g < h, g < j, g < k, h < i, j < n, k < l, k < m
fn select_914([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if k < f {
        select_913([a, d, b, g, e, h, i, j, k, l, m, n])
    } else {
        select_900([a, b, c, d, e, f, g, h, i, j, n])
    }
}
/// n = 16, i = 4, a < f, a < p, b < e, b < i, b < m, c < d, c < g, c < i, g < h, g < m, h < j, i < k, i < l, i < p, l < n, m < o
fn select_915([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if i < g {
        select_909([a, b, c, d, e, f, i, k, l, g, h, m, n, p])
    } else {
        select_914([a, b, c, d, e, f, g, h, j, m, i, k, l, o])
    }
}
/// n = 17, i = 4, a < f, a < g, b < e, b < k, b < o, c < d, c < h, c < k, g < i, h < j, h < o, j < l, k < m, k < n, n < p, o < q
fn select_916([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if g < k {
        select_902([b, a, c, d, f, e, g, h, i, j, l, o, q, k])
    } else {
        select_915([a, b, c, d, e, f, h, j, k, l, m, n, o, p, q, g])
    }
}
/// n = 17, i = 4, a < g, a < i, b < h, b < l, c < f, c < m, d < e, d < l, d < m, h < j, i < k, l < o, m < n, m < p, p < q
fn select_917([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if b < c {
        select_868([a, d, b, e, g, h, i, c, f, j, k, l, o, m, n, p])
    } else {
        select_916([a, d, c, f, e, g, i, b, k, h, m, j, n, p, l, q, o])
    }
}
/// n = 5, i = 3, c < e, d < e
fn select_918([a, b, c, d, e]: [usize; 5]) -> usize {
    if a < b {
        select_71([c, d, a, b, e])
    } else {
        select_71([c, d, b, a, e])
    }
}
/// n = 6, i = 3, c < f, d < e, e < f
fn select_919([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if e < a {
        select_102([b, c, e, a, f])
    } else {
        select_918([b, c, a, d, e])
    }
}
/// n = 8, i = 3, a < d, b < e, c < e, e < f, e < g, e < h
fn select_920([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_4([a, f, g, h])
    } else {
        select_44([d, b, c, e])
    }
}
/// n = 8, i = 3, c < e, d < e, e < f, e < g, e < h
fn select_921([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_920([a, c, d, b, e, f, g, h])
    } else {
        select_920([b, c, d, a, e, f, g, h])
    }
}
/// n = 10, i = 3, b < e, c < f, d < f, d < j, e < j, f < g, f < h, f < i
fn select_922([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_919([a, c, d, b, e, j])
    } else {
        select_921([a, b, c, d, f, g, h, i])
    }
}
/// n = 10, i = 2, a < j, b < d, b < i, b < j, c < e, c < i, e < f, e < g, e < h
fn select_923([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < b {
        select_49([a, e, b, f, g, h])
    } else {
        select_739([a, c, b, d, e, i, j])
    }
}
/// n = 11, i = 3, b < k, c < f, c < j, d < e, d < f, e < j, e < k, f < g, f < h, f < i
fn select_924([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_923([b, e, c, a, f, g, h, i, j, k])
    } else {
        select_801([b, a, c, d, e, f, g, h, i])
    }
}
/// n = 11, i = 3, b < e, c < g, c < k, d < f, d < g, f < k, g < h, g < i, g < j
fn select_925([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_922([a, b, c, d, e, g, h, i, j, f])
    } else {
        select_924([a, b, c, d, f, g, h, i, j, k, e])
    }
}
/// n = 11, i = 3, b < g, c < f, c < h, d < e, d < h, h < i, h < j, h < k
fn select_926([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_925([a, b, c, d, g, e, h, i, j, k, f])
    } else {
        select_925([a, b, d, c, g, f, h, i, j, k, e])
    }
}
/// n = 7, i = 3, a < f, a < g, b < e, b < g, c < d, c < f, c < g
fn select_927([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < e {
        select_79([d, b, a, f, g, e])
    } else {
        select_766([a, c, b, e, f, d, g])
    }
}
/// n = 9, i = 3, a < f, b < e, b < g, c < d, c < f, c < g, g < h, g < i
fn select_928([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < a {
        select_212([d, e, g, a, h, i])
    } else {
        select_927([a, b, c, d, e, f, g])
    }
}
/// n = 10, i = 3, b < e, b < g, b < j, c < d, c < f, c < g, f < j, g < h, g < i
fn select_929([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_540([d, f, b, e, a, g, h, i, j])
    } else {
        select_928([a, b, c, d, e, f, g, h, i])
    }
}
/// n = 12, i = 4, a < d, a < e, a < j, b < c, b < f, e < i, f < g, f < h, f < j, j < k, j < l
fn select_930([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < e {
        select_929([c, a, f, h, d, g, j, k, l, e])
    } else {
        select_56([b, a, d, c, e, f, h, i, j, k, l, g])
    }
}
/// n = 12, i = 4, a < d, a < g, b < c, b < e, b < f, e < i, f < h, f < l, g < j, g < k, g < l
fn select_931([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < g {
        select_926([c, e, a, f, h, d, i, g, j, k, l])
    } else {
        select_930([b, a, d, c, e, g, j, k, i, f, h, l])
    }
}
/// n = 14, i = 4, a < d, a < f, a < l, b < c, b < e, b < g, e < i, f < j, f < k, g < h, g < l, l < m, l < n
fn select_932([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if l < f {
        select_926([c, e, a, g, h, d, i, l, f, m, n])
    } else {
        select_931([a, b, c, d, e, g, f, h, i, j, k, l])
    }
}
/// n = 8, i = 1, c < g, c < h, d < e, d < f
fn select_933([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_212([a, b, c, d, g, h])
    } else {
        select_212([a, b, d, c, e, f])
    }
}
/// n = 8, i = 2, b < h, c < d, c < e, c < h, e < f, e < g
fn select_934([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < b {
        select_212([a, d, e, b, f, g])
    } else {
        select_260([a, b, c, d, e, h])
    }
}
/// n = 9, i = 2, c < d, c < e, c < f, e < i, f < g, f < h
fn select_935([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_933([b, d, e, f, g, h, a, i])
    } else {
        select_934([b, a, c, d, f, g, h, e])
    }
}
/// n = 11, i = 3, b < e, b < f, c < d, c < g, c < k, f < k, g < h, g < i, i < j
fn select_936([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < b {
        select_935([a, d, g, h, i, b, e, f, j])
    } else {
        select_929([a, c, b, e, d, f, g, h, i, k])
    }
}
/// n = 10, i = 2, a < j, b < h, b < i, c < d, c < h, c < i, c < j, d < e, d < f, d < g
fn select_937([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < b {
        select_23([a, d, b, e, f, g, j])
    } else {
        select_434([a, b, c, d, h, i, j])
    }
}
/// n = 10, i = 2, b < i, b < j, c < d, c < e, c < i, c < j, e < f, e < g, e < h
fn select_938([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_7([d, b, e, f, g, h, i, j, a])
    } else {
        select_937([a, b, c, e, f, g, h, i, j, d])
    }
}
/// n = 8, i = 2, a < h, b < g, c < e, c < f, d < e, d < f, d < g, d < h
fn select_939([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_243([c, a, d, b, h, e, f])
    } else {
        select_243([c, b, d, a, g, e, f])
    }
}
/// n = 9, i = 3, a < i, b < e, b < h, b < i, c < d, c < f, c < g, c < i, d < h, e < f, e < g
fn select_940([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_150([e, c, a, d, h, f, g])
    } else {
        select_766([a, b, c, d, e, h, i])
    }
}
/// n = 9, i = 3, a < i, b < e, b < g, b < h, b < i, c < d, c < f, c < i, f < g, f < h
fn select_941([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_939([a, d, f, b, g, h, e, i])
    } else {
        select_940([a, c, b, e, f, g, h, d, i])
    }
}
/// n = 11, i = 3, b < e, b < g, b < j, b < k, c < d, c < f, c < g, f < j, f < k, g < h, g < i
fn select_942([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_938([d, f, b, e, g, a, h, i, j, k])
    } else {
        select_941([a, b, c, d, e, f, j, k, g])
    }
}
/// n = 10, i = 2, a < f, b < e, b < j, c < d, c < g, c < j, g < h, g < i
fn select_943([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_659([a, c, d, f, b, g, h, i, e])
    } else {
        select_41([b, c, d, e, a, g, h, i, f, j])
    }
}
/// n = 11, i = 3, b < e, b < h, b < k, c < d, c < f, c < h, f < g, f < k, h < i, h < j
fn select_944([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_943([d, f, b, e, g, a, h, i, j, k])
    } else {
        select_48([a, b, c, e, f, g, d, h, i, j, k])
    }
}
/// n = 12, i = 3, b < e, b < g, b < i, c < d, c < f, c < i, c < l, f < h, g < l, i < j, i < k
fn select_945([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < f {
        select_942([a, c, b, e, d, g, i, j, k, f, l])
    } else {
        select_944([a, b, c, d, e, f, h, i, j, k, g])
    }
}
/// n = 14, i = 3, b < e, b < f, b < j, c < d, c < g, c < j, c < n, f < n, g < h, g < i, i < k, j < l, j < m
fn select_946([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < j {
        select_936([a, b, c, d, e, f, g, h, i, k, n])
    } else {
        select_945([a, b, c, d, e, g, f, h, j, l, m, n])
    }
}
/// n = 8, i = 3, b < e, b < f, c < d, c < f, f < g, f < h
fn select_947([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_338([a, d, b, f, g, h, e])
    } else {
        select_338([a, e, c, f, g, h, d])
    }
}
/// n = 8, i = 3, b < e, b < h, c < d, c < f, f < g, f < h
fn select_948([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < b {
        select_21([a, d, f, g, b, e, h])
    } else {
        select_947([a, b, c, d, e, f, g, h])
    }
}
/// n = 9, i = 2, a < f, b < e, b < i, c < d, c < g, c < i, g < h
fn select_949([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_693([a, c, d, f, g, b, h, e])
    } else {
        select_910([b, c, d, e, g, a, h, f, i])
    }
}
/// n = 9, i = 3, a < c, a < g, b < d, b < g, c < f, d < e, d < h, h < i
fn select_950([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if h < c {
        select_62([a, d, e, g, h, i])
    } else {
        select_663([a, b, d, c, e, f, g])
    }
}
/// n = 10, i = 3, a < g, b < d, b < j, c < e, c < g, e < f, e < h, e < j, h < i
fn select_951([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_950([a, c, b, e, f, d, g, h, i])
    } else {
        select_441([b, c, d, a, e, f, h, i, j, g])
    }
}
/// n = 10, i = 3, b < e, b < j, c < d, c < f, f < g, f < h, f < j, h < i
fn select_952([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_949([d, b, f, g, e, a, h, i, j])
    } else {
        select_951([a, b, c, e, f, g, d, h, i, j])
    }
}
/// n = 11, i = 3, b < e, b < f, c < d, c < g, f < i, g < h, g < j, j < k
fn select_953([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < g {
        select_948([a, c, b, e, d, f, i, g])
    } else {
        select_952([a, b, c, d, e, g, h, j, k, f])
    }
}
/// n = 12, i = 3, b < e, b < g, b < j, c < d, c < f, c < j, f < h, g < i, j < k, j < l
fn select_954([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < g {
        select_944([a, b, c, d, e, f, h, j, k, l, g])
    } else {
        select_944([a, c, b, e, d, g, i, j, k, l, f])
    }
}
/// n = 14, i = 3, b < e, b < f, b < k, c < d, c < g, c < k, f < i, g < h, g < j, j < l, k < m, k < n
fn select_955([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if j < k {
        select_953([a, b, c, d, e, f, g, h, i, j, l])
    } else {
        select_954([a, b, c, d, e, g, f, h, i, k, m, n])
    }
}
/// n = 16, i = 4, a < d, a < f, a < k, b < c, b < e, b < k, b < p, e < g, e < i, f < h, f < j, i < l, j < p, k < m, k < n, n < o
fn select_956([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if f < e {
        select_946([d, f, b, c, h, j, k, m, n, e, o, g, i, p])
    } else {
        select_955([c, e, a, d, g, i, k, m, l, n, f, o, h, j])
    }
}
/// n = 16, i = 4, a < f, a < g, b < e, b < l, b < p, c < d, c < h, c < l, g < j, h < i, h < k, k < p, l < m, l < n, n < o
fn select_957([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_932([c, a, f, d, g, h, b, e, j, i, k, l, m, n])
    } else {
        select_956([c, b, e, d, a, h, f, i, g, k, l, j, m, n, o, p])
    }
}
/// n = 9, i = 3, a < d, a < e, b < f, b < i, c < e, c < f, d < i, f < g, f < h
fn select_958([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < f {
        select_104([b, d, c, e, i])
    } else {
        select_237([a, b, e, f, g, h])
    }
}
/// n = 10, i = 3, a < f, a < j, b < d, b < e, c < e, c < f, d < j, e < g, f < h, f < i
fn select_959([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < f {
        select_131([a, d, c, e, g, j])
    } else {
        select_310([b, a, e, f, h, i, g])
    }
}
/// n = 10, i = 3, a < e, b < f, c < e, c < g, d < f, d < g, f < j, g < h, g < i
fn select_960([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_958([a, d, c, b, e, g, h, i, f])
    } else {
        select_959([c, b, d, a, f, g, j, h, i, e])
    }
}
/// n = 11, i = 3, a < f, b < f, b < g, b < j, c < d, c < g, d < e, d < j, f < k, g < h, g < i
fn select_961([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_578([d, b, a, e, g, h, i, j])
    } else {
        select_842([a, b, c, d, f, g, h, i, e, k])
    }
}
/// n = 11, i = 3, b < f, c < e, c < g, d < f, d < g, d < j, e < j, f < k, g < h, g < i
fn select_962([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < e {
        select_960([a, b, c, d, e, f, g, h, i, k])
    } else {
        select_961([b, d, c, e, a, f, g, h, i, j, k])
    }
}
/// n = 9, i = 2, a < e, a < i, b < c, b < d, b < i, d < f, e < g, e < h
fn select_963([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_42([c, a, d, f, i])
    } else {
        select_242([b, a, c, e, g, h, i])
    }
}
/// n = 9, i = 2, a < e, b < c, b < d, c < g, d < f, e < h, e < i
fn select_964([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < a {
        select_27([d, c, a, g, f])
    } else {
        select_134([b, a, d, e, h, i, f, c])
    }
}
/// n = 10, i = 2, a < e, b < d, b < j, c < f, c < j, e < i, f < g, f < h
fn select_965([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < a {
        select_963([c, b, d, a, f, e, g, h, j])
    } else {
        select_964([c, a, b, e, f, i, d, g, h])
    }
}
/// n = 8, i = 3, a < e, b < e, b < f, b < h, c < d, c < f, d < h, f < g
fn select_966([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_90([d, b, a, f, g, h])
    } else {
        select_108([a, b, c, d, e, f, g])
    }
}
/// n = 9, i = 3, a < e, b < e, b < f, b < i, c < d, c < f, d < i, f < g, f < h
fn select_967([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_24([d, f, a, g, h, i])
    } else {
        select_766([a, b, c, d, e, i, f])
    }
}
/// n = 10, i = 3, a < e, b < f, c < g, d < e, d < f, d < g, f < j, g < h, g < i
fn select_968([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < c {
        select_966([a, d, b, c, e, f, j, g])
    } else {
        select_967([a, d, c, b, e, g, h, i, f])
    }
}
/// n = 11, i = 3, b < f, c < g, c < j, d < e, d < f, d < g, e < j, f < k, g < h, g < i
fn select_969([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_965([b, e, c, a, f, g, h, i, k, j])
    } else {
        select_968([a, b, c, d, e, f, g, h, i, k])
    }
}
/// n = 11, i = 3, b < g, c < f, c < h, d < e, d < g, d < h, g < k, h < i, h < j
fn select_970([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < e {
        select_962([a, b, c, d, f, g, h, i, j, e, k])
    } else {
        select_969([a, b, c, d, e, g, h, i, j, f, k])
    }
}
/// n = 9, i = 2, a < i, b < e, c < d, c < f, c < i, f < g, f < h
fn select_971([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < b {
        select_149([d, a, f, b, g, h, i])
    } else {
        select_81([a, b, c, d, e, f, i])
    }
}
/// n = 9, i = 2, c < i, d < e, d < f, d < i, f < g, f < h
fn select_972([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_971([c, a, d, e, b, f, g, h, i])
    } else {
        select_971([c, b, d, e, a, f, g, h, i])
    }
}
/// n = 10, i = 2, a < c, a < j, b < d, b < e, b < j, d < h, d < i, e < f, e < g
fn select_973([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_5([e, d, a, h, i, f, g])
    } else {
        select_152([a, b, c, e, f, g, d, j])
    }
}
/// n = 10, i = 2, b < d, b < j, c < e, c < f, c < j, e < i, f < g, f < h
fn select_974([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < e {
        select_539([a, b, c, d, f, g, h, j, e])
    } else {
        select_973([b, c, d, e, f, g, h, a, i, j])
    }
}
/// n = 8, i = 3, a < h, b < e, c < f, c < h, d < e, d < f, d < h, f < g
fn select_975([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < a {
        select_307([c, b, d, a, e, f, g])
    } else {
        select_828([c, a, d, b, f, g, e, h])
    }
}
/// n = 10, i = 3, b < e, c < f, c < g, d < e, d < f, d < g, f < j, g < h, g < i
fn select_976([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_379([b, c, e, f, g, a, h, i, j])
    } else {
        select_975([a, b, c, d, e, f, j, g])
    }
}
/// n = 11, i = 3, c < f, c < g, c < k, d < e, d < f, d < g, e < k, f < j, g < h, g < i
fn select_977([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_974([b, e, c, a, f, g, h, i, j, k])
    } else {
        select_976([b, a, c, d, e, f, g, h, i, j])
    }
}
/// n = 11, i = 3, c < f, c < g, c < h, d < e, d < g, d < h, g < k, h < i, h < j
fn select_978([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_977([a, b, c, d, e, g, h, i, j, k, f])
    } else {
        select_977([a, b, d, c, f, g, h, i, j, k, e])
    }
}
/// n = 12, i = 3, b < l, c < f, c < i, d < e, d < g, d < i, g < h, g < l, i < j, i < k
fn select_979([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < c {
        select_972([a, e, b, g, h, c, f, i, l])
    } else {
        select_978([a, b, c, d, e, f, g, i, j, k, h])
    }
}
/// n = 14, i = 3, b < i, b < m, c < f, c < i, c < j, d < e, d < g, d < j, g < h, g < m, i < n, j < k, j < l
fn select_980([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < g {
        select_970([a, b, d, c, f, e, i, j, k, l, n])
    } else {
        select_979([a, b, c, d, e, f, g, h, j, k, l, m])
    }
}
/// n = 7, i = 2, a < d, a < e, b < c, b < f, f < g
fn select_981([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < f {
        select_107([b, a, d, e, c])
    } else {
        select_62([a, b, c, e, f, g])
    }
}
/// n = 8, i = 2, a < h, b < e, c < d, c < f, c < h, f < g
fn select_982([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < a {
        select_981([b, c, d, a, e, f, g])
    } else {
        select_575([a, c, d, f, b, g, e, h])
    }
}
/// n = 8, i = 2, c < h, d < e, d < f, d < h, f < g
fn select_983([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_982([c, a, d, e, b, f, g, h])
    } else {
        select_982([c, b, d, e, a, f, g, h])
    }
}
/// n = 7, i = 2, a < c, a < d, b < e, e < f, e < g
fn select_984([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < e {
        select_83([b, c, d])
    } else {
        select_237([a, b, d, e, f, g])
    }
}
/// n = 8, i = 2, a < c, a < d, b < e, b < f, e < h, f < g
fn select_985([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_984([a, b, c, d, e, f, h])
    } else {
        select_984([a, b, c, d, f, e, g])
    }
}
/// n = 11, i = 3, a < f, a < g, b < d, b < e, b < g, c < d, c < e, c < f, d < i, e < h, f < j, g < k
fn select_986([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_842([a, b, c, f, g, d, e, i, j, k])
    } else {
        select_842([a, b, c, f, g, e, d, h, j, k])
    }
}
/// n = 11, i = 3, a < h, b < f, b < g, b < h, c < d, c < f, c < g, d < e, f < j, g < i, h < k
fn select_987([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_985([d, b, a, e, f, g, i, j])
    } else {
        select_986([a, b, c, f, g, d, h, i, j, e, k])
    }
}
/// n = 11, i = 3, a < e, b < h, c < e, c < f, c < g, d < f, d < g, d < h, f < j, g < i, h < k
fn select_988([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < g {
        select_960([a, b, c, d, e, h, f, g, j, k])
    } else {
        select_960([a, b, c, d, e, h, g, f, i, k])
    }
}
/// n = 11, i = 3, b < h, c < e, c < f, c < g, d < f, d < g, d < h, f < j, g < i, h < k
fn select_989([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_987([b, d, c, e, a, f, g, h, i, j, k])
    } else {
        select_988([a, b, c, d, e, f, g, h, i, j, k])
    }
}
/// n = 12, i = 3, b < i, b < k, c < h, c < i, d < e, d < f, d < h, f < g, f < k, h < j, i < l
fn select_990([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < c {
        select_983([a, e, b, f, g, c, h, k])
    } else {
        select_989([a, b, d, c, e, f, h, i, j, g, l])
    }
}
/// n = 8, i = 3, a < c, a < h, b < d, b < h, c < g, d < e, d < f
fn select_991([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_19([b, c, g, h, d])
    } else {
        select_176([a, d, e, f, h, c])
    }
}
/// n = 9, i = 3, a < h, b < d, b < i, c < e, c < h, e < f, e < g, e < i
fn select_992([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_991([a, c, b, e, f, g, d, h])
    } else {
        select_607([b, c, d, a, e, f, g, i, h])
    }
}
/// n = 10, i = 4, a < f, a < j, b < e, b < g, c < d, c < g, g < h, g < i, g < j
fn select_993([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_992([d, a, b, f, g, h, i, e, j])
    } else {
        select_992([e, a, c, f, g, h, i, d, j])
    }
}
/// n = 9, i = 3, a < e, b < g, c < e, c < f, d < f, d < g, f < h, g < i
fn select_994([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_702([d, c, a, b, e, f, h, g])
    } else {
        select_516([c, d, b, a, g, f, i, h, e])
    }
}
/// n = 8, i = 3, a < c, a < f, b < d, b < f, c < e, d < g, g < h
fn select_995([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < d {
        select_19([b, c, e, f, d])
    } else {
        select_90([a, d, f, g, h, c])
    }
}
/// n = 11, i = 4, a < e, a < h, b < e, b < g, c < d, c < k, d < g, d < h, e < f, e < k, g < i, h < j
fn select_996([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < d {
        select_11([f, c, d, k])
    } else {
        select_137([a, b, g, h, i, j, e])
    }
}
/// n = 11, i = 4, a < g, a < i, b < d, b < h, c < e, c < f, d < f, d < g, e < h, e < i, h < j, i < k
fn select_997([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_995([d, c, a, e, g, f, h, j])
    } else {
        select_996([a, b, c, e, d, g, h, i, j, k, f])
    }
}
/// n = 11, i = 4, a < g, a < i, b < e, b < h, c < d, c < f, e < g, f < h, f < i, h < j, i < k
fn select_998([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_994([d, a, b, f, e, h, i, j, k])
    } else {
        select_997([a, b, c, e, f, d, g, h, i, j, k])
    }
}
/// n = 11, i = 4, a < f, a < i, b < e, b < h, c < d, c < g, g < h, g < i, h < j, i < k
fn select_999([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_998([a, b, c, d, e, g, f, h, i, j, k])
    } else {
        select_998([b, a, c, d, f, g, e, i, h, k, j])
    }
}
/// n = 12, i = 4, a < f, a < j, a < l, b < e, b < h, c < d, c < g, c < h, g < j, h < i, h < l, j < k
fn select_1000([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < g {
        select_993([a, b, c, d, e, f, h, g, i, l])
    } else {
        select_999([a, b, c, d, e, f, g, h, j, i, k])
    }
}
/// n = 14, i = 4, a < f, a < k, a < n, b < e, b < h, b < j, c < d, c < g, c < h, g < j, g < k, h < i, h < n, j < l, k < m
fn select_1001([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if j < f {
        select_990([d, a, g, b, e, h, i, j, k, l, n, m])
    } else {
        select_1000([a, b, c, d, e, f, g, h, i, k, m, n])
    }
}
/// n = 16, i = 4, a < f, a < k, b < e, b < j, b < l, c < d, c < g, c < h, g < j, g < k, h < i, h < l, j < o, k < p, l < m, l < n
fn select_1002([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if h < a {
        select_980([d, g, b, h, i, e, a, f, j, l, m, n, k, o])
    } else {
        select_1001([b, a, c, d, f, e, g, h, i, k, j, p, o, l])
    }
}
/// n = 8, i = 2, b < g, b < h, c < d, c < g, c < h, d < e, d < f
fn select_1003([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_5([b, d, a, e, f, g, h])
    } else {
        select_259([a, b, c, g, h, d])
    }
}
/// n = 10, i = 3, b < e, b < g, c < d, c < g, c < j, d < f, e < j, g < h, g < i
fn select_1004([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < d {
        select_1003([a, e, c, g, h, i, d, j])
    } else {
        select_619([a, d, b, f, g, h, i, e])
    }
}
/// n = 10, i = 3, b < e, c < g, c < j, d < f, d < g, f < j, g < h, g < i
fn select_1005([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < c {
        select_106([a, d, b, e, f, c, g])
    } else {
        select_1004([a, d, c, b, f, e, g, h, i, j])
    }
}
/// n = 11, i = 4, a < e, b < f, b < h, c < d, c < g, f < k, g < h, g < k, h < i, h < j
fn select_1006([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < g {
        select_402([b, a, c, d, e, f, g, h])
    } else {
        select_1004([d, b, g, a, f, e, h, i, j, k])
    }
}
/// n = 11, i = 4, a < f, b < e, b < i, c < d, c < g, g < h, g < i, i < j, i < k
fn select_1007([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < e {
        select_1005([d, a, b, g, f, h, i, j, k, e])
    } else {
        select_1006([a, b, c, d, f, e, g, i, j, k, h])
    }
}
/// n = 9, i = 3, a < g, b < d, b < h, b < i, c < e, c < g, e < f, e < h, e < i
fn select_1008([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_153([b, e, f, d, a, g, h, i])
    } else {
        select_74([b, a, c, d, g, e, f])
    }
}
/// n = 10, i = 4, a < f, a < i, a < j, b < e, b < g, c < d, c < g, g < h, g < i, g < j
fn select_1009([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_1008([d, a, b, f, g, h, e, i, j])
    } else {
        select_1008([e, a, c, f, g, h, d, i, j])
    }
}
/// n = 11, i = 4, a < f, a < i, b < e, b < i, c < d, c < g, c < k, g < h, i < j, i < k
fn select_1010([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < i {
        select_778([a, b, c, d, e, f, g, h, i])
    } else {
        select_1009([c, a, b, e, f, d, i, j, g, k])
    }
}
/// n = 8, i = 3, a < d, a < h, b < f, b < g, b < h, c < e, c < f, c < h, e < g
fn select_1011([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < d {
        select_234([a, e, b, f, g, h, d])
    } else {
        select_766([b, c, a, d, f, e, h])
    }
}
/// n = 9, i = 3, a < d, a < i, b < g, b < h, b < i, c < e, c < g, c < i, e < f, e < h
fn select_1012([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_39([b, e, f, g, a, d, h])
    } else {
        select_779([b, c, a, d, g, e, f, i])
    }
}
/// n = 9, i = 3, a < e, a < i, b < d, b < h, b < i, c < f, c < h, c < i, f < g
fn select_1013([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < f {
        select_1011([a, c, b, e, d, h, f, i])
    } else {
        select_1012([a, b, c, e, f, g, h, d, i])
    }
}
/// n = 7, i = 4, a < g, b < f, b < g, c < e, c < g, d < e, d < f
fn select_1014([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < f {
        select_96([a, b, d, e, g, f])
    } else {
        select_96([a, c, d, f, g, e])
    }
}
/// n = 8, i = 4, a < f, b < g, b < h, c < f, c < g, c < h, d < e, d < g, e < h
fn select_1015([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_766([b, c, e, a, g, f, h])
    } else {
        select_1014([b, c, d, a, e, f, g])
    }
}
/// n = 8, i = 3, a < d, b < g, b < h, c < e, c < g, e < f, e < h
fn select_1016([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_39([b, e, f, g, a, d, h])
    } else {
        select_695([b, c, a, d, g, e, f])
    }
}
/// n = 9, i = 4, a < f, b < e, b < i, c < g, c < i, d < f, d < g, d < i, g < h
fn select_1017([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < g {
        select_1015([a, c, d, b, e, f, i, g])
    } else {
        select_1016([a, b, c, f, g, h, i, e])
    }
}
/// n = 10, i = 4, b < e, b < i, b < j, c < g, c < i, c < j, d < f, d < g, d < i, f < j, g < h
fn select_1018([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_1013([f, b, c, e, a, g, h, i, j])
    } else {
        select_1017([a, b, c, d, e, f, g, h, i])
    }
}
/// n = 8, i = 3, a < h, b < f, c < e, c < h, d < e, d < f, d < h, f < g
fn select_1019([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < b {
        select_80([a, b, d, e, f, h])
    } else {
        select_256([a, c, d, f, g, e])
    }
}
/// n = 9, i = 3, a < g, b < f, b < g, b < h, c < d, c < f, d < e, d < h, g < i
fn select_1020([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_176([b, d, a, e, f, h])
    } else {
        select_872([b, c, a, f, d, g, e, i])
    }
}
/// n = 10, i = 4, a < i, b < f, b < h, c < e, c < h, c < i, d < f, d < h, d < i, f < g, i < j
fn select_1021([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_1019([e, a, b, d, h, i, j, f])
    } else {
        select_1020([a, c, b, f, g, h, i, e, j])
    }
}
/// n = 11, i = 4, a < e, a < j, b < c, b < d, b < i, d < f, d < j, d < k, e < g, e < i, e < k, g < h
fn select_1022([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_34([c, f, a, j, e, g, i, k])
    } else {
        select_623([g, b, c, i, h, d, f, j, k])
    }
}
/// n = 12, i = 5, a < e, a < g, a < k, b < g, b < i, b < k, c < d, c < f, f < i, f < k, f < l, g < h, g < l, i < j
fn select_1023([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < g {
        select_1021([d, f, a, b, e, i, j, k, g, h])
    } else {
        select_1022([c, a, e, g, f, h, i, j, k, d, l])
    }
}
/// n = 12, i = 5, a < e, a < h, a < l, b < h, b < j, b < l, c < d, c < f, f < g, f < j, f < l, h < i, j < k
fn select_1024([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < h {
        select_1018([d, a, b, f, e, g, j, k, l, h])
    } else {
        select_1023([a, b, c, d, e, f, h, i, j, k, l, g])
    }
}
/// n = 12, i = 5, a < e, a < j, a < l, b < d, b < g, c < f, c < j, c < l, f < h, g < i, g < l, j < k
fn select_1025([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < g {
        select_1010([b, f, a, e, h, d, j, k, g, i, l])
    } else {
        select_1024([a, c, b, d, e, g, i, j, k, f, h, l])
    }
}
/// n = 15, i = 5, a < e, a < f, b < d, b < j, b < l, c < g, c < j, c < l, f < i, f < l, g < h, g < m, j < k, j < m, m < n, m < o
fn select_1026([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if m < f {
        select_1007([a, g, b, d, h, e, j, k, m, n, o])
    } else {
        select_1025([b, a, c, e, d, g, f, h, i, j, k, l])
    }
}
/// n = 17, i = 5, a < e, a < f, b < d, b < j, b < k, c < g, c < j, c < k, f < i, g < h, g < m, g < n, j < m, k < l, k < n, m < q, n < o, n < p
fn select_1027([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if j < f {
        select_1002([a, g, b, d, h, e, j, k, l, m, f, n, o, p, q, i])
    } else {
        select_1026([a, b, c, d, e, f, g, h, i, k, l, j, n, o, p])
    }
}
/// n = 18, i = 5, a < e, a < f, b < d, b < l, c < g, c < h, c < l, f < k, g < j, g < m, h < i, h < m, h < p, l < p, m < n, m < o, o < q, p < r
fn select_1028([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if g < b {
        select_957([a, h, g, j, i, e, f, b, d, k, l, m, n, o, q, p])
    } else {
        select_1027([a, b, c, d, e, f, h, i, k, l, g, j, p, m, n, o, r])
    }
}
/// n = 18, i = 5, a < e, b < d, b < f, c < g, c < h, c < i, f < l, g < m, h < k, h < n, i < j, i < m, i < n, m < p, n < o, n < q, q < r
fn select_1029([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if g < a {
        select_917([b, g, h, i, j, k, d, a, f, e, l, m, n, o, p, q, r])
    } else {
        select_1028([b, a, c, e, d, f, h, i, j, k, l, g, n, o, q, m, r, p])
    }
}
/// n = 11, i = 2, c < f, c < k, d < e, d < g, d < k, f < j, g < h, g < i
fn select_1030([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_837([a, c, d, e, b, f, g, h, i, j, k])
    } else {
        select_837([b, c, d, e, a, f, g, h, i, j, k])
    }
}
/// n = 14, i = 3, a < g, a < j, b < e, b < f, b < i, c < d, c < i, c < j, g < h, i < k, i < l, j < m, j < n
fn select_1031([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if a < b {
        select_850([g, b, c, d, e, f, h, j, m, n, i])
    } else {
        select_1030([e, f, a, c, d, g, i, k, l, h, j])
    }
}
/// n = 8, i = 2, a < e, b < c, b < d, b < f, f < g, f < h
fn select_1032([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < a {
        select_212([c, d, f, a, g, h])
    } else {
        select_176([a, b, c, d, e, f])
    }
}
/// n = 10, i = 2, a < d, b < c, b < e, b < f, e < i, e < j, f < g, f < h
fn select_1033([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_33([a, b, c, d, e, f, i, j])
    } else {
        select_33([a, b, c, d, f, e, g, h])
    }
}
/// n = 10, i = 2, a < g, b < e, b < f, c < d, c < h, h < i, h < j
fn select_1034([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < c {
        select_1032([a, b, e, f, g, c, d, h])
    } else {
        select_1033([a, c, d, g, b, h, i, j, e, f])
    }
}
/// n = 10, i = 2, c < f, c < g, d < e, d < h, h < i, h < j
fn select_1035([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_1034([a, c, d, e, f, g, b, h, i, j])
    } else {
        select_1034([b, c, d, e, f, g, a, h, i, j])
    }
}
/// n = 10, i = 3, b < d, b < i, b < j, c < e, c < f, e < j, f < g, f < h, f < i
fn select_1036([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_484([e, b, f, g, h, d, a, i, j])
    } else {
        select_992([a, b, c, d, f, g, h, e, i])
    }
}
/// n = 13, i = 4, a < e, a < i, b < d, b < j, b < m, c < f, c < i, f < g, f < h, f < j, i < m, j < k, j < l
fn select_1037([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if f < a {
        select_1035([g, h, a, b, d, e, i, j, k, l])
    } else {
        select_1036([e, b, c, d, i, f, g, h, j, m])
    }
}
/// n = 15, i = 4, a < e, b < d, b < j, b < k, c < f, c < g, f < k, g < h, g < i, g < j, j < l, j < m, k < n, k < o
fn select_1038([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if f < a {
        select_1031([f, g, b, d, h, i, a, e, j, k, l, m, n, o])
    } else {
        select_1037([a, b, c, d, e, g, h, i, f, j, l, m, k])
    }
}
/// n = 8, i = 2, c < d, d < e, d < f, d < g, d < h
fn select_1039([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_128([a, c, b, d, e, f, g, h])
    } else {
        select_128([b, c, a, d, e, f, g, h])
    }
}
/// n = 8, i = 3, a < c, a < d, a < h, b < e, e < f, e < h, f < g
fn select_1040([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if c < e {
        select_44([d, b, c, e])
    } else {
        select_150([a, e, d, f, g, c, h])
    }
}
/// n = 10, i = 3, a < c, a < d, a < j, b < e, e < f, e < g, e < j, f < i, g < h
fn select_1041([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < c {
        select_574([a, e, d, f, g, h, i, j])
    } else {
        select_1040([a, b, c, d, e, g, h, j])
    }
}
/// n = 10, i = 3, a < c, a < d, a < j, b < e, e < f, e < g, e < h, e < j, h < i
fn select_1042([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < g {
        select_1041([a, b, c, d, e, f, h, i, g, j])
    } else {
        select_1041([a, b, c, d, e, g, h, i, f, j])
    }
}
/// n = 13, i = 3, a < c, a < d, a < i, b < e, b < i, e < f, e < g, e < h, h < j, i < k, i < l, i < m
fn select_1043([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if i < e {
        select_1039([c, d, b, i, e, k, l, m])
    } else {
        select_1042([a, b, c, d, e, f, g, h, j, i])
    }
}
/// n = 7, i = 1, a < g, b < f, c < d, c < e
fn select_1044([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_151([a, c, d, e, b, g])
    } else {
        select_151([b, c, d, e, a, f])
    }
}
/// n = 7, i = 1, c < g, d < e, d < f
fn select_1045([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_1044([a, c, d, e, f, g, b])
    } else {
        select_1044([b, c, d, e, f, g, a])
    }
}
/// n = 7, i = 1, b < f, b < g, c < d, c < e
fn select_1046([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if b < c {
        select_18([a, b, c, f, g])
    } else {
        select_18([a, c, b, d, e])
    }
}
/// n = 8, i = 2, c < d, c < e, d < h, e < f, e < g
fn select_1047([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_1046([b, d, e, f, g, a, h])
    } else {
        select_338([b, a, c, e, f, g, d])
    }
}
/// n = 10, i = 3, a < c, a < d, a < j, b < e, b < f, e < i, e < j, f < g, f < h, f < i
fn select_1048([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_1045([g, h, e, a, c, d, i])
    } else {
        select_1047([c, d, b, e, f, g, h, j])
    }
}
/// n = 7, i = 3, a < e, b < c, b < d, b < g, e < f, e < g
fn select_1049([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < d {
        select_277([a, b, c, e, f, d, g])
    } else {
        select_277([a, b, d, e, f, c, g])
    }
}
/// n = 8, i = 3, a < c, a < d, a < h, b < e, e < f, e < g, e < h
fn select_1050([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < c {
        select_176([a, e, f, g, d, h])
    } else {
        select_1049([b, a, c, d, e, g, h])
    }
}
/// n = 10, i = 3, a < c, a < d, b < e, e < f, e < g, e < h, h < i, h < j
fn select_1051([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < a {
        select_212([f, g, h, a, i, j])
    } else {
        select_1050([a, b, c, d, e, f, g, h])
    }
}
/// n = 11, i = 3, a < c, a < d, a < k, b < e, b < f, e < k, f < g, f < h, f < i, i < j
fn select_1052([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < i {
        select_1048([a, b, c, d, e, f, g, h, i, k])
    } else {
        select_1051([a, b, c, d, f, g, h, i, e, j])
    }
}
/// n = 12, i = 3, a < c, a < i, b < d, b < i, c < g, d < e, d < f, d < h, h < j, i < k, i < l
fn select_1053([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < a {
        select_1045([e, f, h, a, c, i, j])
    } else {
        select_190([c, b, g, i, d, e, f, h, k, l])
    }
}
/// n = 12, i = 3, a < c, a < l, b < d, b < e, c < i, d < h, d < l, e < f, e < g, e < j, j < k
fn select_1054([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < a {
        select_613([d, e, f, g, h, j, a, k, c, l])
    } else {
        select_1053([a, b, c, e, f, g, i, j, d, k, h, l])
    }
}
/// n = 14, i = 4, a < c, a < h, b < d, b < h, c < g, c < n, d < e, d < f, d < n, g < i, h < j, h < k, h < l, l < m
fn select_1055([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if e < g {
        select_1052([d, a, e, f, c, h, j, k, l, m, n])
    } else {
        select_1054([c, b, g, d, h, j, k, f, i, l, m, n])
    }
}
/// n = 16, i = 4, a < d, a < h, b < c, b < h, b < m, c < g, d < e, d < f, d < m, g < i, h < j, h < k, h < l, l < n, m < o, m < p
fn select_1056([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if m < c {
        select_1043([d, b, e, f, h, j, k, l, m, n, c, o, p])
    } else {
        select_1055([b, a, c, d, e, f, g, h, i, j, k, l, n, m])
    }
}
/// n = 10, i = 1, b < h, b < i, b < j, c < d, c < e, c < f, c < g
fn select_1057([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_23([a, c, d, e, f, g, b])
    } else {
        select_758([b, c, d, e, f, g, a, h, i, j])
    }
}
/// n = 11, i = 2, c < d, c < e, d < j, d < k, e < f, e < g, e < h, e < i
fn select_1058([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_1057([b, d, e, f, g, h, i, a, j, k])
    } else {
        select_228([b, a, c, e, f, g, h, i, d])
    }
}
/// n = 15, i = 3, a < c, a < d, a < j, b < e, b < j, e < f, e < g, e < h, e < i, h < m, i < k, i < l, j < n, j < o
fn select_1059([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if e < a {
        select_200([f, g, h, i, a, c, d, j, k, l, m])
    } else {
        select_1058([c, d, b, j, e, f, g, h, i, n, o])
    }
}
/// n = 9, i = 4, a < e, b < c, b < d, d < f, d < i, e < g, e < h, e < i
fn select_1060([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < c {
        select_53([b, e, h, g, d, f, i, c])
    } else {
        select_687([c, d, a, f, e, h, i, g])
    }
}
/// n = 7, i = 2, c < d, d < e, d < f, d < g
fn select_1061([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_418([a, c, b, d, e, f, g])
    } else {
        select_418([b, c, a, d, e, f, g])
    }
}
/// n = 9, i = 4, a < d, b < c, c < e, c < f, c < i, d < g, d < h, d < i
fn select_1062([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < g {
        select_1049([a, c, e, f, d, h, i])
    } else {
        select_1049([b, d, g, h, c, f, i])
    }
}
/// n = 11, i = 4, a < d, b < c, b < i, c < g, c < h, d < e, d < f, d < i, i < j, i < k
fn select_1063([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if i < c {
        select_1061([e, f, b, i, c, j, k])
    } else {
        select_1062([a, b, c, d, g, h, e, f, i])
    }
}
/// n = 11, i = 4, a < d, a < h, b < h, b < i, c < e, e < f, e < g, e < i, i < j, i < k
fn select_1064([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1060([c, a, d, b, e, h, f, g, i])
    } else {
        select_1063([c, b, a, e, f, g, d, h, i, j, k])
    }
}
/// n = 7, i = 2, c < f, c < g, d < e, d < f, d < g
fn select_1065([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_869([a, c, d, e, b, f, g])
    } else {
        select_869([b, c, d, e, a, f, g])
    }
}
/// n = 11, i = 3, a < c, a < d, a < h, b < e, b < h, e < f, e < g, h < i, h < j, h < k
fn select_1066([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < e {
        select_1039([c, d, b, h, e, i, j, k])
    } else {
        select_1050([a, b, c, d, e, f, g, h])
    }
}
/// n = 12, i = 4, a < h, a < i, b < d, b < h, b < i, c < e, c < i, e < f, e < g, i < j, i < k, i < l
fn select_1067([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < a {
        select_1065([f, g, a, b, d, h, i])
    } else {
        select_1066([b, c, d, h, e, f, g, i, j, k, l])
    }
}
/// n = 15, i = 4, a < d, a < h, a < j, b < h, b < i, b < j, c < e, c < j, e < f, e < g, e < i, i < k, i < l, j < m, j < n, j < o
fn select_1068([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if i < j {
        select_1064([a, b, c, d, e, f, g, h, i, k, l])
    } else {
        select_1067([b, a, c, d, e, f, g, h, j, m, n, o])
    }
}
/// n = 16, i = 4, a < d, a < h, b < h, b < i, b < m, c < e, c < i, e < f, e < g, e < m, i < j, i < k, i < l, l < n, m < o, m < p
fn select_1069([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if i < a {
        select_1059([e, b, f, g, i, j, k, l, a, m, d, h, n, o, p])
    } else {
        select_1068([a, b, c, d, e, f, g, h, m, i, o, p, j, k, l])
    }
}
/// n = 16, i = 4, a < e, b < d, b < i, b < m, c < f, c < i, f < g, f < h, f < m, i < j, i < k, i < l, l < n, m < o, m < p
fn select_1070([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if d < a {
        select_1056([c, b, d, f, g, h, a, i, e, j, k, l, m, n, o, p])
    } else {
        select_1069([a, b, c, e, f, g, h, d, i, j, k, l, m, n, o, p])
    }
}
/// n = 16, i = 4, a < f, b < e, b < j, b < m, c < d, c < g, c < j, g < h, g < i, g < m, j < k, j < l, l < n, m < o, m < p
fn select_1071([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if d < j {
        select_1038([a, b, c, e, f, d, g, h, i, m, j, o, p, k, l])
    } else {
        select_1070([a, b, c, e, f, g, h, i, j, d, k, l, m, n, o, p])
    }
}
/// n = 10, i = 2, a < d, b < c, b < e, b < f, e < j, f < g, f < h, f < i
fn select_1072([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_146([c, e, f, g, h, i, a, j])
    } else {
        select_50([a, b, c, d, f, g, h, i, e])
    }
}
/// n = 12, i = 2, a < f, b < e, b < g, b < l, c < d, c < h, c < l, g < k, h < i, h < j
fn select_1073([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if b < c {
        select_1072([a, b, e, f, g, c, d, h, l, k])
    } else {
        select_656([a, c, d, f, h, b, e, g, l, i, j])
    }
}
/// n = 12, i = 2, b < e, b < f, b < l, c < d, c < g, c < l, e < k, f < j, g < h, g < i
fn select_1074([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if b < c {
        select_147([a, e, f, c, d, g, l, j, k])
    } else {
        select_8([a, d, g, b, e, f, l, h, i])
    }
}
/// n = 12, i = 2, b < f, c < g, c < l, d < e, d < h, d < l, g < k, h < i, h < j
fn select_1075([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if b < c {
        select_585([a, b, d, e, f, c, h, i, j, g])
    } else {
        select_1074([a, c, d, e, b, g, h, i, j, k, f, l])
    }
}
/// n = 15, i = 3, a < g, a < k, b < e, b < f, b < j, c < d, c < j, c < k, f < h, g < i, j < l, j < m, k < n, k < o
fn select_1076([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if a < b {
        select_1073([g, b, c, d, e, i, f, k, n, o, h, j])
    } else {
        select_1075([e, f, a, c, d, h, g, j, l, m, i, k])
    }
}
/// n = 8, i = 3, a < e, b < d, c < e, c < f, c < g, d < f, d < g, e < h
fn select_1077([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_11([a, c, f, g])
    } else {
        select_84([b, c, d, e, h])
    }
}
/// n = 9, i = 3, a < e, b < f, b < h, c < d, c < f, c < i, d < h, e < i, f < g
fn select_1078([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_286([a, d, b, f, g, h, e])
    } else {
        select_1077([b, a, c, e, f, d, i, g])
    }
}
/// n = 10, i = 3, a < d, a < i, b < f, b < h, b < j, c < e, c < f, d < j, e < h, e < i, f < g
fn select_1079([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_286([d, b, c, e, i, f, j])
    } else {
        select_888([a, c, e, f, d, g, h, j])
    }
}
/// n = 10, i = 3, a < f, a < j, b < e, b < g, c < d, c < g, c < i, e < j, f < i, g < h
fn select_1080([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_1078([a, b, c, d, f, g, h, e, i])
    } else {
        select_1079([a, c, b, f, e, g, h, d, j, i])
    }
}
/// n = 10, i = 3, a < d, a < j, b < g, b < i, c < e, c < f, e < i, f < h, g < j
fn select_1081([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_583([e, b, f, h, g, a, d, i])
    } else {
        select_1080([b, c, a, d, e, g, f, h, j, i])
    }
}
/// n = 8, i = 3, a < d, b < g, b < h, c < e, e < f, e < g, e < h
fn select_1082([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_275([c, a, b, d, e, f])
    } else {
        select_238([c, b, a, e, f, d, g, h])
    }
}
/// n = 8, i = 4, a < d, b < f, c < e, e < g, e < h, f < g, f < h
fn select_1083([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < d {
        select_386([a, e, b, f, d, g, h])
    } else {
        select_71([c, d, b, f, e])
    }
}
/// n = 10, i = 4, a < d, b < e, b < i, c < f, e < j, f < g, f < j, g < h, g < i
fn select_1084([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < e {
        select_1082([a, b, f, d, g, h, e, i])
    } else {
        select_1083([a, b, c, d, f, e, g, j])
    }
}
/// n = 10, i = 4, a < d, a < j, b < f, b < g, c < e, c < g, e < i, f < h, f < i, g < h, g < j
fn select_1085([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < e {
        select_687([f, a, c, d, g, e, j, h])
    } else {
        select_272([a, c, b, d, f, e, g, i])
    }
}
/// n = 11, i = 4, a < d, a < k, b < e, b < h, c < f, c < h, e < j, f < g, f < j, g < i, h < k
fn select_1086([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < h {
        select_1084([a, b, c, d, e, f, g, i, h, j])
    } else {
        select_1085([a, c, b, d, e, f, h, g, j, k])
    }
}
/// n = 11, i = 4, a < e, a < k, b < d, b < i, c < f, c < i, f < g, f < h, h < j, i < k
fn select_1087([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < d {
        select_1081([a, b, f, e, g, h, i, j, d, k])
    } else {
        select_1086([a, b, c, e, d, f, h, i, j, g, k])
    }
}
/// n = 9, i = 3, b < d, b < i, c < e, e < f, e < g, e < i, g < h
fn select_1088([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < a {
        select_40([b, e, f, d, g, a, h, i])
    } else {
        select_687([a, b, c, d, e, f, i, g])
    }
}
/// n = 10, i = 3, b < d, b < j, c < e, e < f, e < g, e < j, g < h, g < i
fn select_1089([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_50([b, e, f, d, g, a, h, i, j])
    } else {
        select_687([a, b, c, d, e, f, j, g])
    }
}
/// n = 12, i = 4, a < e, a < h, b < d, b < i, c < f, f < g, f < h, f < i, h < l, i < j, i < k
fn select_1090([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_1088([e, b, c, d, f, g, h, l, i])
    } else {
        select_1089([d, a, c, e, f, g, i, j, k, h])
    }
}
/// n = 12, i = 4, a < e, b < d, b < j, c < f, f < g, f < h, f < j, h < i, j < k, j < l
fn select_1091([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < a {
        select_585([g, h, b, d, i, a, j, k, l, e])
    } else {
        select_1090([a, b, c, d, e, f, g, h, j, k, l, i])
    }
}
/// n = 14, i = 4, a < e, a < i, b < d, b < k, b < n, c < f, c < i, f < g, f < h, f < k, h < j, i < n, k < l, k < m
fn select_1092([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < k {
        select_1087([b, a, c, e, d, f, g, h, i, j, n])
    } else {
        select_1091([a, b, c, d, e, f, g, h, j, k, l, m])
    }
}
/// n = 16, i = 4, a < e, b < d, b < k, b < l, c < f, c < g, f < l, g < h, g < i, g < k, i < j, k < m, k < n, l < o, l < p
fn select_1093([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if f < a {
        select_1076([f, g, b, d, h, i, a, j, e, k, l, m, n, o, p])
    } else {
        select_1092([a, b, c, d, e, g, h, i, f, j, k, m, n, l])
    }
}
/// n = 9, i = 2, b < d, b < h, b < i, c < e, c < h, c < i, e < f, e < g
fn select_1094([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < e {
        select_427([a, c, b, d, h, i, e])
    } else {
        select_861([b, c, d, e, a, f, g, h, i])
    }
}
/// n = 14, i = 3, a < c, a < d, a < j, b < e, b < j, b < n, d < h, d < n, e < f, e < g, e < i, i < k, j < l, j < m
fn select_1095([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if d < e {
        select_1094([c, d, b, h, j, l, m, e, n])
    } else {
        select_572([a, e, f, g, c, i, j, k, l, m, d])
    }
}
/// n = 9, i = 1, b < i, c < g, c < h, d < e, d < f
fn select_1096([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_149([a, b, c, d, g, h, i])
    } else {
        select_149([a, b, d, c, e, f, i])
    }
}
/// n = 11, i = 2, a < j, a < k, b < e, b < f, b < k, c < d, c < g, c < j, g < h, g < i
fn select_1097([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < c {
        select_1045([e, f, a, c, d, g, k])
    } else {
        select_1096([d, a, b, g, h, i, e, f, j])
    }
}
/// n = 11, i = 2, a < e, a < g, b < c, b < d, b < f, f < h, f < i, g < j, g < k
fn select_1098([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_212([c, d, f, a, h, i])
    } else {
        select_483([b, a, e, c, d, g, j, k, f])
    }
}
/// n = 12, i = 2, a < l, b < e, b < f, b < g, c < d, c < h, c < l, g < k, h < i, h < j
fn select_1099([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < g {
        select_1097([a, b, c, d, e, f, h, i, j, l, g])
    } else {
        select_1098([c, b, e, f, d, g, h, a, k, i, j])
    }
}
/// n = 15, i = 3, a < c, a < o, b < d, b < e, c < i, d < g, d < h, d < j, e < f, e < k, e < o, j < n, k < l, k < m
fn select_1100([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if k < c {
        select_1099([a, d, e, f, g, h, j, k, l, m, n, o])
    } else {
        select_1054([a, b, c, e, d, g, h, f, i, j, n, o])
    }
}
/// n = 17, i = 4, a < c, a < h, a < n, b < d, b < h, c < g, d < e, d < f, d < n, f < i, g < j, h < k, h < l, h < m, m < o, n < p, n < q
fn select_1101([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if f < c {
        select_1095([d, a, e, f, h, k, l, i, m, n, o, p, q, c])
    } else {
        select_1100([c, b, g, h, d, e, k, l, j, m, n, p, q, o, f])
    }
}
/// n = 12, i = 2, b < d, c < e, c < f, e < k, e < l, f < g, f < h, f < i, f < j
fn select_1102([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < b {
        select_1057([a, e, f, g, h, i, j, b, k, l])
    } else {
        select_175([a, b, c, d, f, g, h, i, j, e])
    }
}
/// n = 16, i = 3, a < c, a < d, a < k, b < e, b < k, d < h, e < f, e < g, e < i, e < j, i < n, j < l, j < m, k < o, k < p
fn select_1103([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < a {
        select_200([f, g, i, j, a, c, d, k, l, m, n])
    } else {
        select_1102([c, d, b, h, k, e, f, g, i, j, o, p])
    }
}
/// n = 9, i = 2, a < f, b < c, b < d, b < e, e < g, f < h, f < i
fn select_1104([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_173([c, d, e, a, g])
    } else {
        select_578([b, a, c, d, f, h, i, e])
    }
}
/// n = 9, i = 2, a < c, a < g, a < h, a < i, b < d, b < g, b < h, b < i, d < e, d < f
fn select_1105([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_18([c, b, g, h, i])
    } else {
        select_5([d, a, g, h, i, e, f])
    }
}
/// n = 11, i = 2, a < e, a < j, a < k, b < c, b < d, b < j, b < k, d < f, d < g, e < h, e < i
fn select_1106([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_18([c, d, a, f, g])
    } else {
        select_1105([b, a, c, e, h, i, d, j, k])
    }
}
/// n = 11, i = 2, a < e, a < f, b < d, b < j, b < k, c < g, c < j, c < k, g < h, g < i
fn select_1107([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1104([c, a, e, f, b, g, d, h, i])
    } else {
        select_1106([c, b, d, a, g, e, f, h, i, j, k])
    }
}
/// n = 10, i = 2, a < e, a < i, a < j, b < c, b < d, b < i, b < j, d < f, e < g, e < h
fn select_1108([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_316([c, d, a, i, j, f])
    } else {
        select_152([b, a, c, e, g, h, i, j])
    }
}
/// n = 11, i = 2, a < e, b < d, b < i, b < j, c < f, c < i, c < j, e < k, f < g, f < h
fn select_1109([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_964([c, a, b, e, f, k, d, g, h])
    } else {
        select_1108([c, b, d, a, f, e, g, h, i, j])
    }
}
/// n = 11, i = 2, b < f, c < e, c < j, c < k, d < g, d < j, d < k, g < h, g < i
fn select_1110([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < a {
        select_1107([b, c, d, e, a, f, g, h, i, j, k])
    } else {
        select_1109([a, c, d, e, b, g, h, i, j, k, f])
    }
}
/// n = 11, i = 2, c < d, c < e, d < i, d < j, d < k, e < f, e < g, e < h
fn select_1111([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_1039([a, b, c, d, e, i, j, k])
    } else {
        select_1039([a, b, c, e, d, f, g, h])
    }
}
/// n = 13, i = 3, b < d, b < h, b < m, c < e, c < h, e < f, e < g, e < m, g < i, h < j, h < k, h < l
fn select_1112([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if e < b {
        select_566([a, f, g, b, d, h, m, i])
    } else {
        select_1111([a, d, c, e, h, j, k, l, f, g, m])
    }
}
/// n = 16, i = 4, a < d, a < g, a < k, b < g, b < j, b < k, c < e, c < k, e < f, e < h, e < j, h < i, j < l, j < m, k < n, k < o, k < p
fn select_1113([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < a {
        select_1110([f, h, a, b, d, i, j, l, m, g, k])
    } else {
        select_1112([d, b, c, g, e, f, h, k, i, n, o, p, j])
    }
}
/// n = 17, i = 4, a < d, a < g, b < g, b < i, b < n, c < e, c < i, e < f, e < h, e < n, h < j, i < k, i < l, i < m, m < o, n < p, n < q
fn select_1114([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if i < a {
        select_1103([e, b, f, h, i, k, l, j, m, a, n, d, g, o, p, q])
    } else {
        select_1113([a, b, c, d, e, f, g, h, j, n, i, p, q, k, l, m])
    }
}
/// n = 17, i = 4, a < e, b < d, b < i, b < n, c < f, c < i, f < g, f < h, f < n, h < j, i < k, i < l, i < m, m < o, n < p, n < q
fn select_1115([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if d < a {
        select_1101([b, c, d, f, g, h, a, i, j, e, k, l, m, n, o, p, q])
    } else {
        select_1114([a, b, c, e, f, g, d, h, i, j, k, l, m, n, o, p, q])
    }
}
/// n = 17, i = 4, a < f, b < e, b < j, b < n, c < d, c < g, c < j, g < h, g < i, g < n, i < k, j < l, j < m, m < o, n < p, n < q
fn select_1116([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if d < j {
        select_1093([a, b, c, e, f, d, g, h, i, k, n, j, p, q, l, m])
    } else {
        select_1115([a, b, c, e, f, g, h, i, j, k, d, l, m, n, o, p, q])
    }
}
/// n = 17, i = 4, a < f, b < e, b < g, b < m, c < d, c < h, c < m, g < j, g < k, h < i, h < l, l < n, m < o, m < p, p < q
fn select_1117([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if g < h {
        select_1071([a, c, b, e, d, f, g, j, k, m, o, p, h, q, i, l])
    } else {
        select_1116([a, b, c, d, e, f, h, i, l, m, n, o, p, g, q, j, k])
    }
}
/// n = 14, i = 4, a < f, b < e, b < j, b < k, c < d, c < g, g < h, g < i, g < j, g < k, j < n, k < l, k < m
fn select_1118([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if h < i {
        select_914([a, b, c, d, e, f, g, h, i, j, k, l, m, n])
    } else {
        select_914([a, b, c, d, e, f, g, i, h, j, k, l, m, n])
    }
}
/// n = 11, i = 1, c < i, c < j, c < k, d < e, d < f, d < g, d < h
fn select_1119([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_759([a, c, d, e, f, g, h, i, j, k, b])
    } else {
        select_759([b, c, d, e, f, g, h, i, j, k, a])
    }
}
/// n = 11, i = 3, a < k, b < e, b < f, b < k, c < d, c < f, c < k, f < g, f < h, f < i, f < j
fn select_1120([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_504([a, d, b, f, g, h, i, j, e, k])
    } else {
        select_504([a, e, c, f, g, h, i, j, d, k])
    }
}
/// n = 13, i = 3, b < e, b < f, b < g, c < d, c < f, c < g, f < l, f < m, g < h, g < i, g < j, g < k
fn select_1121([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if f < a {
        select_1119([d, e, f, g, h, i, j, k, a, l, m])
    } else {
        select_1120([a, b, c, d, e, g, h, i, j, k, f])
    }
}
/// n = 14, i = 3, b < e, b < h, b < i, c < d, c < f, c < h, c < i, f < g, h < m, h < n, i < j, i < k, i < l
fn select_1122([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if f < i {
        select_944([a, b, c, d, e, f, g, h, m, n, i])
    } else {
        select_1121([a, b, c, d, e, h, i, f, j, k, l, m, n])
    }
}
/// n = 15, i = 4, a < f, b < e, b < i, b < j, c < d, c < g, g < h, g < i, g < j, i < n, i < o, j < k, j < l, j < m
fn select_1123([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < a {
        select_1122([d, b, g, h, e, a, f, i, j, k, l, m, n, o])
    } else {
        select_1009([b, a, c, d, f, e, g, h, i, j])
    }
}
/// n = 16, i = 4, a < f, b < e, b < h, b < l, c < d, c < g, c < m, g < i, g < j, g < l, h < k, h < m, l < p, m < n, m < o
fn select_1124([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if g < h {
        select_1118([a, b, c, d, e, f, g, i, j, l, h, k, m, p])
    } else {
        select_1123([a, c, b, e, d, f, h, k, m, g, i, j, l, n, o])
    }
}
/// n = 14, i = 4, a < f, b < e, b < k, b < n, c < d, c < g, g < h, g < i, g < k, i < j, i < n, k < l, k < m
fn select_1125([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if a < b {
        select_536([a, c, d, f, b, g, h, e, i, j, k])
    } else {
        select_57([b, c, d, e, a, g, h, f, i, j, k, l, m, n])
    }
}
/// n = 8, i = 3, a < g, a < h, b < d, b < h, c < e, c < h, d < g, e < f
fn select_1126([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_107([b, e, a, f, d])
    } else {
        select_828([c, b, a, d, e, f, g, h])
    }
}
/// n = 8, i = 3, a < e, a < h, b < d, b < h, c < f, c < h, f < g
fn select_1127([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_1126([a, b, c, d, f, g, e, h])
    } else {
        select_1126([b, a, c, e, f, g, d, h])
    }
}
/// n = 7, i = 3, a < g, b < d, c < e, e < f, e < g
fn select_1128([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < b {
        select_42([f, a, b, d, g])
    } else {
        select_550([a, d, c, e, f])
    }
}
/// n = 7, i = 4, a < g, b < f, c < f, c < g, d < e, e < g
fn select_1129([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < f {
        select_347([a, b, c, e, f, g])
    } else {
        select_44([a, d, f, e])
    }
}
/// n = 8, i = 4, a < f, b < e, c < g, d < f, d < g, g < h
fn select_1130([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if g < e {
        select_1128([b, a, c, f, g, h, e])
    } else {
        select_1129([c, a, d, b, e, f, g])
    }
}
/// n = 9, i = 4, b < e, b < i, c < g, c < i, d < f, d < g, f < i, g < h
fn select_1131([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_1127([b, f, c, a, e, g, h, i])
    } else {
        select_1130([a, b, c, d, e, f, g, h])
    }
}
/// n = 9, i = 3, b < e, b < f, c < d, c < f, f < g, f < h, f < i
fn select_1132([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_606([a, d, b, f, g, h, i, e])
    } else {
        select_606([a, e, c, f, g, h, i, d])
    }
}
/// n = 9, i = 2, b < d, b < i, c < e, c < i, e < f, e < g, e < h
fn select_1133([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < b {
        select_49([a, e, b, f, g, h])
    } else {
        select_260([a, c, b, d, e, i])
    }
}
/// n = 9, i = 3, a < d, a < i, b < e, b < i, c < e, c < i, e < f, e < g, e < h
fn select_1134([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_4([a, f, g, h])
    } else {
        select_52([d, b, c, e, i])
    }
}
/// n = 9, i = 3, b < i, c < e, c < i, d < e, d < i, e < f, e < g, e < h
fn select_1135([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_920([a, c, d, b, e, f, g, h])
    } else {
        select_1134([b, c, d, a, e, f, g, h, i])
    }
}
/// n = 11, i = 4, b < e, b < h, c < f, c < h, d < f, d < h, f < g, h < i, h < j, h < k
fn select_1136([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < e {
        select_1133([a, f, b, g, h, i, j, k, e])
    } else {
        select_1135([a, e, c, d, h, i, j, k, f])
    }
}
/// n = 12, i = 5, a < e, a < g, b < g, b < i, c < d, c < f, f < i, f < k, f < l, g < h, g < k, g < l, i < j
fn select_1137([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < f {
        select_1132([e, c, g, h, d, f, i, k, l])
    } else {
        select_1136([d, a, b, f, e, i, j, g, h, k, l])
    }
}
/// n = 12, i = 5, a < e, a < h, b < h, b < j, c < d, c < f, f < g, f < j, f < l, h < i, h < l, j < k
fn select_1138([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < h {
        select_1131([d, a, b, f, e, g, j, k, h])
    } else {
        select_1137([a, b, c, d, e, f, h, i, j, k, g, l])
    }
}
/// n = 15, i = 5, a < e, b < f, b < j, c < d, c < g, f < i, f < l, f < o, g < h, g < j, g < l, j < k, j < o, l < m, l < n
fn select_1139([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if f < a {
        select_57([f, c, d, i, a, g, h, e, j, k, l, m, n, o])
    } else {
        select_1138([a, b, c, d, e, g, h, f, i, j, k, l])
    }
}
/// n = 17, i = 5, a < e, b < g, b < j, c < d, c < f, c < j, f < h, f < m, g < i, g < l, g < m, j < k, j < l, l < n, l < o, m < p, m < q
fn select_1140([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if j < f {
        select_1125([a, g, c, d, i, e, j, k, f, h, l, n, o, m])
    } else {
        select_1139([a, b, c, d, e, g, f, h, i, j, k, m, p, q, l])
    }
}
/// n = 17, i = 5, a < e, b < d, b < f, b < k, c < g, c < k, f < i, g < h, g < j, g < o, j < l, j < m, k < n, k < o, o < p, o < q
fn select_1141([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if j < f {
        select_1124([a, b, g, h, d, e, j, k, l, m, n, f, o, p, q, i])
    } else {
        select_1140([a, c, b, d, e, f, g, i, h, k, n, o, j, p, q, l, m])
    }
}
/// n = 18, i = 5, a < e, b < d, b < f, c < g, c < h, f < k, g < j, g < o, h < i, h < l, h < o, l < m, l < n, o < p, o < q, q < r
fn select_1142([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if g < b {
        select_1117([a, h, g, j, i, e, l, b, d, m, n, f, o, k, p, q, r])
    } else {
        select_1141([a, b, c, d, e, f, h, i, k, l, g, m, n, j, o, p, q])
    }
}
/// n = 18, i = 5, a < f, b < e, b < g, c < d, c < h, c < i, g < l, h < k, h < o, i < j, i < m, i < o, m < n, o < p, o < q, q < r
fn select_1143([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if d < m {
        select_1029([a, b, c, e, f, g, d, h, i, j, k, l, m, o, p, n, q, r])
    } else {
        select_1142([a, b, c, e, f, g, h, i, j, k, l, m, d, n, o, p, q, r])
    }
}
/// n = 18, i = 5, c < f, c < g, d < e, d < h, d < i, g < l, h < k, h < o, i < j, i < m, i < o, m < n, o < p, o < q, q < r
fn select_1144([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1143([a, c, d, e, f, b, g, h, i, j, k, l, m, n, o, p, q, r])
    } else {
        select_1143([b, c, d, e, f, a, g, h, i, j, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, c < h, d < g, e < f, e < i, e < j, i < l, i < o, j < k, j < m, j < o, m < n, o < p, o < q, q < r
fn select_1145([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if c < d {
        select_1144([a, b, c, e, f, h, d, i, j, k, l, g, m, n, o, p, q, r])
    } else {
        select_1144([a, b, d, e, f, g, c, i, j, k, l, h, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, e < h, f < g, f < i, f < j, i < l, i < o, j < k, j < m, j < o, m < n, o < p, o < q, q < r
fn select_1146([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1145([c, d, a, e, f, g, h, b, i, j, k, l, m, n, o, p, q, r])
    } else {
        select_1145([c, d, b, e, f, g, h, a, i, j, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, g < h, g < i, g < j, i < l, i < o, j < k, j < m, j < o, m < n, o < p, o < q, q < r
fn select_1147([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1146([c, d, e, f, a, g, h, b, i, j, k, l, m, n, o, p, q, r])
    } else {
        select_1146([c, d, e, f, b, g, h, a, i, j, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, g < h, g < i, g < j, i < l, j < k, j < m, j < n, m < p, n < o, n < q, q < r
fn select_1148([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if n < i {
        select_812([a, b, c, d, e, f, g, h, j, k, m, n, o, p, i, q, r, l])
    } else {
        select_1147([a, b, c, d, e, f, g, h, i, j, k, l, m, p, n, o, q, r])
    }
}
/// n = 8, i = 3, a < f, b < e, b < g, c < d, c < g, g < h
fn select_1149([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_510([a, b, c, f, d, g, h, e])
    } else {
        select_510([a, c, b, f, e, g, h, d])
    }
}
/// n = 9, i = 3, a < f, b < e, b < i, c < d, c < g, g < h, g < i
fn select_1150([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < a {
        select_82([d, b, g, h, e, a, f, i])
    } else {
        select_1149([b, a, c, d, f, e, g, h])
    }
}
/// n = 9, i = 3, a < d, a < h, a < i, b < c, b < e, c < i, d < g, e < f, e < h
fn select_1151([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if c < d {
        select_243([c, e, a, f, h, d, i])
    } else {
        select_235([a, b, e, d, f, g, c, h])
    }
}
/// n = 9, i = 3, a < e, a < i, b < c, b < d, b < h, c < i, d < f, e < g, e < h
fn select_1152([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_79([c, a, d, f, e, i])
    } else {
        select_150([e, b, g, c, i, d, h])
    }
}
/// n = 9, i = 3, a < d, a < f, b < c, b < e, b < i, e < h, f < g, f < i
fn select_1153([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < c {
        select_1151([b, a, d, e, f, g, h, i, c])
    } else {
        select_1152([a, b, c, e, f, h, g, i, d])
    }
}
/// n = 10, i = 3, a < f, a < j, b < e, b < i, c < d, c < g, g < h, g < i, g < j
fn select_1154([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_1153([c, a, f, d, b, g, h, e, j])
    } else {
        select_1153([c, b, e, d, a, g, h, f, i])
    }
}
/// n = 11, i = 3, a < f, a < k, b < e, b < g, c < d, c < h, g < j, h < i, h < k
fn select_1155([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < h {
        select_1150([a, c, b, e, d, f, g, j, h])
    } else {
        select_1154([a, b, c, d, e, f, h, i, g, k])
    }
}
/// n = 11, i = 2, b < e, b < f, b < k, c < d, c < g, c < k, f < j, g < h, g < i
fn select_1156([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < c {
        select_566([a, e, f, c, d, g, k, j])
    } else {
        select_8([a, d, g, b, e, f, k, h, i])
    }
}
/// n = 12, i = 3, a < f, b < e, b < i, b < l, c < d, c < g, c < i, g < h, g < l, i < j, i < k
fn select_1157([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < a {
        select_1156([d, g, b, e, h, a, i, j, k, f, l])
    } else {
        select_586([a, b, c, d, e, f, g, i, j, k, h])
    }
}
/// n = 14, i = 3, a < f, a < g, b < e, b < k, b < n, c < d, c < h, c < k, g < j, h < i, h < n, k < l, k < m
fn select_1158([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if g < k {
        select_1155([b, a, c, d, f, e, g, h, i, j, n])
    } else {
        select_1157([a, b, c, d, e, f, h, i, k, l, m, n])
    }
}
/// n = 15, i = 3, a < f, a < i, b < e, b < h, b < m, c < d, c < g, c < m, g < j, h < k, i < l, m < n, m < o
fn select_1159([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < h {
        select_1158([a, b, c, d, e, f, i, g, j, l, m, n, o, h])
    } else {
        select_1158([a, c, b, e, d, f, i, h, k, l, m, n, o, g])
    }
}
/// n = 16, i = 4, a < e, a < j, b < d, b < i, b < n, c < f, c < i, c < j, f < g, f < h, f < n, h < k, i < l, j < m, n < o, n < p
fn select_1160([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < c {
        select_422([b, c, d, j, f, g, h, m, i])
    } else {
        select_1159([a, b, f, g, d, e, h, i, j, k, l, m, n, o, p])
    }
}
/// n = 16, i = 4, a < e, b < d, b < k, b < n, c < f, c < g, c < k, f < i, g < h, g < j, g < n, j < l, k < m, n < o, n < p
fn select_1161([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if f < a {
        select_1159([f, b, g, h, d, i, j, k, a, l, m, e, n, o, p])
    } else {
        select_1160([a, b, c, d, e, g, h, j, k, f, l, m, i, n, o, p])
    }
}
/// n = 9, i = 3, a < f, a < i, b < e, b < g, b < i, c < d, c < g, c < i, g < h
fn select_1162([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_94([a, b, c, f, d, g, h, e, i])
    } else {
        select_94([a, c, b, f, e, g, h, d, i])
    }
}
/// n = 10, i = 4, a < d, a < j, b < f, b < i, c < e, c < i, c < j, e < h, f < g, f < j
fn select_1163([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_1149([a, b, e, h, i, d, f, g])
    } else {
        select_1162([a, c, f, g, i, d, e, h, j])
    }
}
/// n = 12, i = 4, a < e, a < i, b < d, b < j, c < f, c < i, c < j, e < h, f < g, f < l, j < k, j < l
fn select_1164([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if j < e {
        select_1154([a, f, b, d, g, i, j, k, l, e])
    } else {
        select_1163([b, a, c, d, f, e, h, g, i, j])
    }
}
/// n = 15, i = 4, a < e, a < i, b < d, b < j, b < l, c < f, c < i, c < j, e < h, f < g, f < l, f < o, j < k, j < o, l < m, l < n
fn select_1165([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if l < e {
        select_1157([a, f, b, d, g, i, j, k, l, m, n, o])
    } else {
        select_1164([a, b, c, d, e, f, g, h, i, j, k, o])
    }
}
/// n = 10, i = 4, a < d, b < f, b < i, c < e, c < i, e < g, e < j, f < h, f < j
fn select_1166([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_827([a, b, e, g, i, d, f, h, j])
    } else {
        select_827([a, c, f, h, i, d, e, g, j])
    }
}
/// n = 12, i = 4, a < d, a < l, b < e, b < i, c < f, c < i, e < h, f < g, f < j, j < k, j < l
fn select_1167([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if j < e {
        select_1154([a, b, f, g, i, d, j, k, e, l])
    } else {
        select_1166([a, b, c, d, f, e, g, h, i, j])
    }
}
/// n = 15, i = 4, a < e, a < i, b < d, b < l, b < o, c < f, c < i, e < h, f < g, f < j, f < l, j < k, j < o, l < m, l < n
fn select_1168([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if l < e {
        select_1157([a, b, f, g, d, i, j, k, l, m, n, o])
    } else {
        select_1167([b, a, c, d, e, f, g, h, i, j, k, o])
    }
}
/// n = 16, i = 4, a < e, a < i, b < d, b < k, b < n, c < f, c < i, c < k, e < h, f < g, f < j, f < n, j < l, k < m, n < o, n < p
fn select_1169([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if k < j {
        select_1165([a, b, c, d, e, f, g, h, i, k, m, n, o, p, j])
    } else {
        select_1168([a, b, c, d, e, f, g, h, i, j, l, n, o, p, k])
    }
}
/// n = 12, i = 2, b < e, b < l, c < d, c < f, c < g, c < l, f < j, f < k, g < h, g < i
fn select_1170([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < g {
        select_543([a, b, c, d, e, f, g, j, k, l])
    } else {
        select_543([a, b, c, d, e, g, f, h, i, l])
    }
}
/// n = 14, i = 3, a < d, a < f, a < i, a < j, b < c, b < e, b < i, b < j, e < g, f < h, i < m, i < n, j < k, j < l
fn select_1171([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if e < f {
        select_1170([c, e, a, d, g, i, j, k, l, m, n, f])
    } else {
        select_1170([d, f, b, c, h, i, j, k, l, m, n, e])
    }
}
/// n = 15, i = 3, a < d, a < f, a < l, b < c, b < e, b < g, b < l, e < i, f < j, g < h, g < k, k < m, l < n, l < o
fn select_1172([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < a {
        select_594([c, e, g, h, i, k, a, d, f, l, m])
    } else {
        select_1171([a, b, c, d, e, f, i, j, g, l, n, o, h, k])
    }
}
/// n = 10, i = 2, b < e, c < d, c < f, c < g, f < j, g < h, g < i
fn select_1173([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < b {
        select_566([a, d, f, g, b, h, i, j])
    } else {
        select_82([a, b, c, d, e, f, j, g])
    }
}
/// n = 7, i = 3, a < f, b < f, b < g, c < e, c < g, d < e, d < g
fn select_1174([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < a {
        select_79([a, b, d, e, g, f])
    } else {
        select_104([c, d, b, f, e])
    }
}
/// n = 7, i = 3, b < f, b < g, c < f, c < g, d < e, d < g
fn select_1175([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_295([b, c, d, e, a, f, g])
    } else {
        select_1174([a, d, b, c, f, e, g])
    }
}
/// n = 10, i = 3, b < f, c < f, c < g, d < e, d < g, g < h, g < i, g < j
fn select_1176([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < b {
        select_1039([a, e, c, g, b, h, i, j])
    } else {
        select_1175([a, b, c, d, e, f, g])
    }
}
/// n = 11, i = 3, b < h, c < e, c < k, d < f, d < h, f < g, f < i, f < k, i < j
fn select_1177([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < c {
        select_1173([a, b, f, g, h, i, c, e, k, j])
    } else {
        select_1176([a, b, d, c, e, h, f, g, i, k])
    }
}
/// n = 7, i = 3, a < f, b < f, b < g, c < d, d < e, d < g
fn select_1178([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < a {
        select_73([a, e, b, g])
    } else {
        select_84([b, c, f, d, e])
    }
}
/// n = 11, i = 4, a < d, a < f, b < f, b < g, b < j, c < e, c < i, d < i, e < g, e < j, f < h, j < k
fn select_1179([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < e {
        select_1178([d, c, b, f, h, i, e])
    } else {
        select_296([a, b, e, d, g, i, j, k, f])
    }
}
/// n = 8, i = 2, a < h, b < g, b < h, c < d, c < e, c < g, e < f
fn select_1180([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_316([d, b, e, a, f, g])
    } else {
        select_234([a, b, c, d, g, e, h])
    }
}
/// n = 9, i = 3, a < d, a < h, a < i, b < c, b < e, c < f, d < g, e < h, e < i
fn select_1181([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < c {
        select_242([d, b, g, e, h, i, c])
    } else {
        select_243([e, c, a, f, d, h, i])
    }
}
/// n = 11, i = 4, a < f, a < h, b < f, b < g, b < j, c < d, c < e, d < h, e < g, e < j, f < i, j < k
fn select_1182([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_1180([d, a, b, g, j, k, f, h])
    } else {
        select_1181([b, c, d, f, e, h, i, g, j])
    }
}
/// n = 11, i = 4, a < e, a < g, b < g, b < h, b < j, c < d, c < f, f < h, f < j, g < i, j < k
fn select_1183([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < d {
        select_1179([a, b, c, e, f, g, h, i, d, j, k])
    } else {
        select_1182([a, b, c, d, f, g, h, e, i, j, k])
    }
}
/// n = 9, i = 3, a < h, a < i, b < d, b < g, b < i, c < e, c < i, e < f, e < g, e < h
fn select_1184([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_39([b, e, f, d, a, h, g])
    } else {
        select_265([b, a, c, d, e, f, h, i])
    }
}
/// n = 10, i = 3, a < j, b < d, b < i, b < j, c < e, c < j, e < f, e < g, e < i, g < h
fn select_1185([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_40([b, e, f, d, g, a, h, i])
    } else {
        select_1184([a, b, c, d, e, f, i, g, j])
    }
}
/// n = 11, i = 3, a < c, a < d, a < j, b < e, b < k, d < g, d < k, e < f, e < h, e < j, h < i
fn select_1186([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_260([c, b, d, g, e, k])
    } else {
        select_153([a, e, f, c, h, i, d, j])
    }
}
/// n = 12, i = 4, a < e, a < f, a < l, b < d, b < g, c < f, c < g, f < i, g < h, g < j, g < l, j < k
fn select_1187([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < f {
        select_1185([d, a, c, e, g, h, j, k, l, f])
    } else {
        select_1186([a, b, e, f, g, h, i, j, k, l, d])
    }
}
/// n = 12, i = 4, a < e, a < g, a < l, b < g, b < h, b < j, c < d, c < f, c < h, f < j, g < k, h < i, h < l
fn select_1188([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < h {
        select_1183([a, b, c, d, e, f, g, j, k, h, i])
    } else {
        select_1187([a, c, b, d, e, g, h, i, k, f, j, l])
    }
}
/// n = 14, i = 4, a < e, a < g, a < n, b < g, b < h, b < j, c < d, c < f, c < h, f < j, g < k, h < i, h < l, h < n, l < m
fn select_1189([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if l < g {
        select_1177([d, f, a, b, e, h, i, j, l, m, n])
    } else {
        select_1188([a, b, c, d, e, f, g, h, i, j, k, n])
    }
}
/// n = 16, i = 4, a < e, a < f, b < d, b < j, b < n, c < g, c < j, c < m, f < m, g < h, g < i, g < n, i < k, j < l, n < o, n < p
fn select_1190([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if g < a {
        select_1172([b, g, h, d, i, j, a, e, k, l, f, n, m, o, p])
    } else {
        select_1189([b, c, a, e, d, f, j, g, h, m, l, i, k, n])
    }
}
/// n = 16, i = 4, a < i, b < f, c < e, c < k, c < n, d < g, d < i, d < k, g < h, g < j, g < n, j < l, k < m, n < o, n < p
fn select_1191([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if a < b {
        select_1169([a, c, d, e, b, g, h, f, i, j, k, l, m, n, o, p])
    } else {
        select_1190([b, c, d, e, f, a, g, h, j, k, l, m, i, n, o, p])
    }
}
/// n = 16, i = 4, b < g, c < f, c < k, c < n, d < e, d < h, d < k, h < i, h < j, h < n, j < l, k < m, n < o, n < p
fn select_1192([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < a {
        select_1161([b, c, d, f, g, e, h, i, a, j, k, l, m, n, o, p])
    } else {
        select_1191([a, b, c, d, f, g, h, i, e, j, k, l, m, n, o, p])
    }
}
/// n = 9, i = 3, a < e, a < g, b < c, b < d, b < g, e < f, g < h, g < i
fn select_1193([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < e {
        select_1061([c, d, a, g, e, h, i])
    } else {
        select_1049([a, b, c, d, e, f, g])
    }
}
/// n = 10, i = 3, a < e, b < e, b < f, b < g, c < d, c < f, c < g, f < j, g < h, g < i
fn select_1194([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_149([d, f, g, a, h, i, j])
    } else {
        select_779([a, b, c, d, e, f, j, g])
    }
}
/// n = 11, i = 4, a < d, a < i, a < j, b < c, b < e, c < i, d < g, d < h, e < f, e < j, j < k
fn select_1195([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_1193([b, d, g, h, c, i, e, f, j])
    } else {
        select_1194([c, a, e, f, i, j, d, g, h, k])
    }
}
/// n = 8, i = 3, a < d, a < e, b < e, b < f, c < d, c < f, f < g, f < h
fn select_1196([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < a {
        select_3([a, g, h])
    } else {
        select_19([b, c, d, e, f])
    }
}
/// n = 8, i = 3, a < e, a < f, b < f, b < g, c < d, c < e, c < g, g < h
fn select_1197([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < g {
        select_620([b, a, c, d, e, f, g])
    } else {
        select_1196([a, b, c, e, f, g, d, h])
    }
}
/// n = 9, i = 3, a < f, b < f, b < g, b < i, c < d, c < e, c < g, e < i, g < h
fn select_1198([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_397([d, e, b, a, g, h, i])
    } else {
        select_1197([a, b, c, d, e, f, g, h])
    }
}
/// n = 10, i = 4, a < e, a < i, a < j, b < e, b < f, c < d, c < f, d < i, e < h, f < g, f < j
fn select_1199([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < d {
        select_235([a, c, f, e, g, h, d, j])
    } else {
        select_264([d, a, b, f, g, i, j, e])
    }
}
/// n = 11, i = 4, a < g, b < g, b < h, b < j, c < d, c < e, d < h, e < f, e < j, g < i, j < k
fn select_1200([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_1198([d, b, e, f, a, h, j, k, g])
    } else {
        select_1199([b, a, c, d, g, e, f, i, h, j])
    }
}
/// n = 11, i = 4, b < e, b < i, b < j, c < d, c < f, d < i, e < h, f < g, f < j, j < k
fn select_1201([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_1195([b, c, d, e, f, g, a, h, i, j, k])
    } else {
        select_1200([a, b, c, d, f, g, e, i, h, j, k])
    }
}
/// n = 9, i = 3, b < f, c < f, c < g, d < e, d < g, g < h, g < i
fn select_1202([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < g {
        select_791([a, b, c, d, e, f, g])
    } else {
        select_420([b, c, d, e, f, g, a, h, i])
    }
}
/// n = 12, i = 4, b < f, b < i, c < d, c < e, c < j, d < g, e < i, e < l, f < h, f < j, f < l, j < k
fn select_1203([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < f {
        select_1202([a, e, b, d, g, i, f, h, j])
    } else {
        select_831([a, f, c, h, e, i, d, j, k, g, l])
    }
}
/// n = 12, i = 4, b < e, b < f, b < j, c < d, c < g, e < l, f < i, g < h, g < j, g < l, j < k
fn select_1204([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < e {
        select_1201([a, b, c, d, f, g, h, i, e, j, k])
    } else {
        select_1203([a, c, b, f, e, g, i, h, d, j, k, l])
    }
}
/// n = 10, i = 2, a < e, b < c, b < d, b < f, f < g, f < h, f < i, f < j
fn select_1205([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_549([a, b, e, c, f, g, h, i, j, d])
    } else {
        select_549([a, b, e, d, f, g, h, i, j, c])
    }
}
/// n = 10, i = 2, c < d, c < e, c < f, f < g, f < h, f < i, f < j
fn select_1206([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_1205([a, c, d, e, b, f, g, h, i, j])
    } else {
        select_1205([b, c, d, e, a, f, g, h, i, j])
    }
}
/// n = 13, i = 3, b < e, b < j, b < l, b < m, c < d, c < f, c < j, e < i, f < g, f < h, f < l, f < m, j < k
fn select_1207([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if f < b {
        select_1206([a, d, f, g, h, b, e, j, l, m])
    } else {
        select_223([a, c, b, d, e, i, j, f, g, h, l, m, k])
    }
}
/// n = 6, i = 1, a < f, b < e, c < d
fn select_1208([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_27([c, a, b, f, d])
    } else {
        select_27([c, b, a, e, d])
    }
}
/// n = 8, i = 2, a < h, b < e, c < d, c < h, d < f, e < g
fn select_1209([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < c {
        select_42([a, c, e, g, d])
    } else {
        select_1208([a, b, d, f, e, h])
    }
}
/// n = 10, i = 3, a < g, a < j, b < e, b < f, c < d, c < f, c < g, e < j, f < h, g < i
fn select_1210([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_1209([d, a, b, f, g, h, i, e])
    } else {
        select_881([a, c, b, e, f, g, h, d, i, j])
    }
}
/// n = 9, i = 3, a < e, a < i, b < e, b < f, b < g, c < d, d < f, d < g, d < i, e < h
fn select_1211([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_27([a, b, f, g, i])
    } else {
        select_300([b, c, d, e, i, h])
    }
}
/// n = 10, i = 3, a < f, a < h, a < i, b < e, b < f, c < d, c < e, d < h, d < i, e < g, f < j
fn select_1212([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < d {
        select_310([a, c, f, e, d, g, j])
    } else {
        select_1211([b, a, c, d, f, h, i, j, e])
    }
}
/// n = 10, i = 3, a < f, a < g, b < e, b < g, c < d, c < f, c < i, e < i, f < h, g < j
fn select_1213([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_516([b, a, c, d, f, g, h, j, e])
    } else {
        select_1212([c, a, b, e, g, f, j, d, i, h])
    }
}
/// n = 11, i = 3, a < h, b < g, c < f, c < h, d < e, d < f, d < g, f < i, g < j, h < k
fn select_1214([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < a {
        select_1210([c, b, d, e, a, g, f, j, i, h])
    } else {
        select_1213([c, a, d, e, b, f, h, i, g, k])
    }
}
/// n = 8, i = 2, b < e, b < h, c < d, c < h, d < f, e < g
fn select_1215([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_256([a, b, c, d, f, h])
    } else {
        select_256([a, c, b, e, g, h])
    }
}
/// n = 10, i = 2, b < e, c < d, c < f, d < i, e < j, f < g, f < h
fn select_1216([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < b {
        select_149([a, d, f, b, g, h, i])
    } else {
        select_1215([a, b, c, d, e, i, j, f])
    }
}
/// n = 12, i = 4, a < j, b < d, b < i, c < e, c < h, d < g, d < h, e < f, e < i, e < j, i < k, j < l
fn select_1217([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < e {
        select_21([a, g, c, h, e, f, i])
    } else {
        select_1216([f, a, b, i, j, d, g, h, k, l])
    }
}
/// n = 12, i = 4, a < j, b < e, b < i, c < d, c < f, e < h, f < g, f < i, f < j, i < k, j < l
fn select_1218([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < e {
        select_1214([d, a, b, f, g, i, j, e, k, l, h])
    } else {
        select_1217([a, b, c, e, f, g, h, d, i, j, k, l])
    }
}
/// n = 14, i = 4, b < e, b < k, b < m, b < n, c < d, c < f, e < h, f < g, f < i, f < k, i < j, i < m, i < n, k < l
fn select_1219([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if i < a {
        select_1207([d, b, f, g, e, i, a, j, h, k, l, m, n])
    } else {
        select_1218([a, b, c, d, e, f, g, h, k, i, l, j])
    }
}
/// n = 14, i = 4, b < e, b < f, b < l, b < n, c < d, c < g, f < i, g < h, g < j, g < l, j < k, j < n, l < m
fn select_1220([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if e < j {
        select_1204([a, b, c, d, e, f, g, h, i, l, m, j])
    } else {
        select_1219([a, b, c, d, f, g, h, i, j, k, l, m, e, n])
    }
}
/// n = 8, i = 3, a < e, b < e, b < f, c < d, c < f, f < g, f < h
fn select_1221([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < a {
        select_18([d, f, a, g, h])
    } else {
        select_45([a, b, c, d, e, f])
    }
}
/// n = 9, i = 3, a < e, a < f, b < f, b < g, c < d, c < g, g < h, g < i
fn select_1222([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < g {
        select_105([b, c, a, e, d, f])
    } else {
        select_1221([a, b, c, d, f, g, h, i])
    }
}
/// n = 9, i = 3, a < d, b < e, c < e, c < i, d < i, e < f, e < g, e < h
fn select_1223([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_4([a, f, g, h])
    } else {
        select_92([b, d, c, i, e])
    }
}
/// n = 10, i = 4, a < f, b < g, b < j, c < e, c < g, d < f, d < g, f < j, g < h, g < i
fn select_1224([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < g {
        select_348([b, a, c, d, e, f, j, g])
    } else {
        select_1223([a, c, b, f, g, e, h, i, j])
    }
}
/// n = 10, i = 4, b < g, b < h, c < e, c < h, d < f, d < h, f < g, h < i, h < j
fn select_1225([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_1222([f, b, c, e, a, g, h, i, j])
    } else {
        select_1224([a, b, c, d, e, f, h, i, j, g])
    }
}
/// n = 10, i = 4, b < g, b < h, c < f, c < h, d < e, d < h, h < i, h < j
fn select_1226([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_1225([a, c, b, d, g, e, f, h, i, j])
    } else {
        select_1225([a, d, b, c, g, f, e, h, i, j])
    }
}
/// n = 8, i = 3, b < e, c < f, d < e, d < f, f < g, f < h
fn select_1227([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < f {
        select_773([a, c, b, d, e, f])
    } else {
        select_418([b, c, e, f, a, g, h])
    }
}
/// n = 9, i = 3, c < f, c < i, d < e, d < f, e < i, f < g, f < h
fn select_1228([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_619([b, e, c, a, f, g, h, i])
    } else {
        select_1227([b, a, c, d, e, f, g, h])
    }
}
/// n = 9, i = 3, c < f, c < g, d < e, d < g, g < h, g < i
fn select_1229([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < f {
        select_1228([a, b, c, d, e, g, h, i, f])
    } else {
        select_1228([a, b, d, c, f, g, h, i, e])
    }
}
/// n = 11, i = 5, a < f, a < i, b < e, b < i, c < d, c < g, g < h, g < k, i < j, i < k
fn select_1230([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < i {
        select_1226([d, a, b, g, h, e, f, i, j, k])
    } else {
        select_1229([e, f, c, i, j, d, g, h, k])
    }
}
/// n = 8, i = 4, a < f, b < g, b < h, c < f, c < h, d < e, e < g, e < h
fn select_1231([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_406([b, c, d, f, e, g])
    } else {
        select_79([a, c, b, g, h, f])
    }
}
/// n = 9, i = 4, a < g, b < g, b < h, b < i, c < f, c < i, d < e, d < h, e < i, f < h
fn select_1232([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < f {
        select_1231([a, c, b, d, e, g, f, i])
    } else {
        select_1231([a, d, b, c, f, g, e, h])
    }
}
/// n = 8, i = 4, a < h, b < f, c < f, c < g, c < h, d < e, e < g, e < h
fn select_1233([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < e {
        select_271([a, d, c, f, e, g])
    } else {
        select_80([a, b, c, g, f, h])
    }
}
/// n = 10, i = 4, a < f, b < h, b < i, b < j, c < f, c < g, c < j, d < e, d < g, e < j, g < h, g < i
fn select_1234([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < g {
        select_1233([b, a, c, d, e, f, g, j])
    } else {
        select_1082([a, b, d, f, g, e, h, i])
    }
}
/// n = 10, i = 4, a < g, b < e, b < i, b < j, c < g, c < h, c < j, d < f, d < h, f < j, h < i
fn select_1235([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < h {
        select_1232([a, c, b, d, f, e, g, h, j])
    } else {
        select_1234([a, b, c, d, f, g, h, e, i, j])
    }
}
/// n = 8, i = 2, a < h, b < e, b < g, c < d, c < g, c < h, e < f
fn select_1236([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < c {
        select_316([a, e, c, d, g, f])
    } else {
        select_316([d, a, b, e, g, h])
    }
}
/// n = 9, i = 2, b < f, b < i, c < d, c < e, c < i, e < g, f < h
fn select_1237([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < e {
        select_1236([a, b, c, d, f, h, i, e])
    } else {
        select_359([b, c, d, f, e, a, g, h, i])
    }
}
/// n = 10, i = 4, a < f, b < g, b < i, c < f, c < g, c < i, d < e, d < g, d < j, e < i, f < j, g < h
fn select_1238([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_365([b, c, d, e, f, j, g])
    } else {
        select_966([a, c, d, e, f, g, h, i])
    }
}
/// n = 10, i = 4, a < g, b < f, b < h, c < e, c < h, c < j, d < f, d < g, d < h, g < j, h < i
fn select_1239([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_363([a, c, b, f, g, h, i, e, j])
    } else {
        select_1238([a, b, d, c, e, g, h, i, f, j])
    }
}
/// n = 11, i = 4, a < f, b < g, b < j, c < e, c < h, c < k, d < f, d < g, d < h, g < k, h < i, h < j
fn select_1240([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < a {
        select_1237([e, b, h, i, a, g, f, k, j])
    } else {
        select_1239([b, a, c, d, e, f, g, h, i, k])
    }
}
/// n = 11, i = 4, a < g, b < f, b < i, c < e, c < h, c < k, d < g, d < h, d < i, h < j, i < k
fn select_1241([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < h {
        select_1235([a, c, d, b, e, f, g, i, k, h])
    } else {
        select_1240([a, b, c, d, e, g, i, h, j, f, k])
    }
}
/// n = 9, i = 4, a < d, b < f, c < e, c < g, e < i, f < g, f < i, g < h
fn select_1242([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < f {
        select_271([d, b, c, e, f, g])
    } else {
        select_364([a, c, d, e, g, h, i])
    }
}
/// n = 9, i = 4, a < e, b < d, b < h, c < f, f < g, f < h, h < i
fn select_1243([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < d {
        select_510([a, b, f, e, g, h, i, d])
    } else {
        select_1242([a, c, b, e, d, f, h, i, g])
    }
}
/// n = 10, i = 4, a < e, a < j, b < d, b < h, c < f, c < h, f < g, h < i, h < j
fn select_1244([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < f {
        select_1088([d, a, c, e, h, i, f, g, j])
    } else {
        select_1243([a, b, c, d, e, f, g, h, i])
    }
}
/// n = 8, i = 3, a < h, b < e, b < h, c < d, c < f, c < g, c < h, e < f, e < g
fn select_1245([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_38([c, e, a, d, f, g])
    } else {
        select_45([a, b, c, d, e, h])
    }
}
/// n = 10, i = 4, a < e, a < g, b < f, b < g, c < d, c < f, c < i, c < j, f < h, g < i, g < j
fn select_1246([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_619([d, f, a, h, g, i, j, e])
    } else {
        select_1245([e, b, c, d, g, i, j, f])
    }
}
/// n = 8, i = 4, a < d, a < e, b < f, b < g, c < f, c < g, g < h
fn select_1247([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < g {
        select_800([e, d, b, c, f, g])
    } else {
        select_103([f, a, g, h, e, d])
    }
}
/// n = 11, i = 5, a < d, a < h, b < f, b < i, c < e, c < h, e < i, f < g, f < j, f < k, h < j, h < k
fn select_1248([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < e {
        select_1246([a, c, f, g, d, e, h, i, j, k])
    } else {
        select_1247([a, b, e, d, h, i, f, g])
    }
}
/// n = 12, i = 5, a < d, a < h, b < f, b < i, c < e, c < h, c < j, e < i, f < g, f < j, f < l, h < l, j < k
fn select_1249([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if j < h {
        select_1244([a, f, c, g, d, e, i, j, k, h])
    } else {
        select_1248([a, b, c, d, e, f, g, h, i, j, l])
    }
}
/// n = 12, i = 5, a < f, a < i, b < e, b < i, b < j, c < d, c < g, g < h, g < j, g < l, i < l, j < k
fn select_1250([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < e {
        select_1241([d, a, g, b, h, f, e, j, i, k, l])
    } else {
        select_1249([a, c, b, f, e, g, h, i, d, j, k, l])
    }
}
/// n = 13, i = 5, a < f, a < i, b < e, b < i, b < k, c < d, c < g, g < h, g < k, g < m, i < j, i < m, k < l
fn select_1251([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if j < k {
        select_1230([a, b, c, d, e, f, g, h, i, j, m])
    } else {
        select_1250([a, b, c, d, e, f, g, h, i, k, l, m])
    }
}
/// n = 15, i = 5, a < f, b < e, b < h, c < d, c < g, c < k, g < j, g < m, g < o, h < i, h < k, h < m, k < l, k < o, m < n
fn select_1252([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < a {
        select_1220([d, g, b, e, j, a, h, i, f, k, l, m, n, o])
    } else {
        select_1251([a, c, b, e, d, f, h, i, g, j, k, l, m])
    }
}
/// n = 9, i = 3, b < d, b < g, b < i, c < e, c < g, e < f, e < i, g < h
fn select_1253([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < a {
        select_40([e, b, d, f, g, a, h, i])
    } else {
        select_249([a, b, c, d, e, f, i, g])
    }
}
/// n = 9, i = 3, b < f, b < i, c < g, c < i, d < e, d < g, d < i, g < h
fn select_1254([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if b < c {
        select_871([a, d, b, f, e, c, g, i])
    } else {
        select_1253([a, d, c, e, b, f, g, h, i])
    }
}
/// n = 8, i = 2, a < g, b < f, b < h, c < d, c < e, c < h
fn select_1255([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_981([c, a, g, d, e, b, f])
    } else {
        select_601([c, b, f, d, e, a, g, h])
    }
}
/// n = 9, i = 3, b < e, b < i, c < d, c < f, f < g, f < h, f < i
fn select_1256([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_1255([d, b, f, g, h, e, a, i])
    } else {
        select_992([a, b, c, e, f, g, h, d, i])
    }
}
/// n = 10, i = 3, b < j, c < f, c < i, c < j, d < e, d < g, d < j, g < h, g < i
fn select_1257([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < g {
        select_1254([a, c, b, d, e, f, g, h, j])
    } else {
        select_1256([a, c, d, e, f, g, b, h, i])
    }
}
/// n = 8, i = 3, a < d, a < e, b < f, c < e, c < f, f < g, f < h
fn select_1258([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < f {
        select_306([b, d, c, e])
    } else {
        select_237([a, b, e, f, g, h])
    }
}
/// n = 9, i = 3, a < d, a < i, b < e, b < i, c < e, c < h, c < i, d < h, e < f, e < g
fn select_1259([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < d {
        select_27([a, e, f, g, i])
    } else {
        select_92([b, d, c, h, i])
    }
}
/// n = 9, i = 3, a < i, b < e, c < f, c < i, d < e, d < f, d < i, f < g, f < h
fn select_1260([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if b < a {
        select_1258([b, c, d, a, e, f, g, h])
    } else {
        select_1259([a, c, d, b, f, g, h, e, i])
    }
}
/// n = 10, i = 3, b < j, c < f, c < i, c < j, d < e, d < f, d < j, e < i, f < g, f < h
fn select_1261([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_539([b, e, c, a, f, g, h, i, j])
    } else {
        select_1260([b, a, c, d, e, f, g, h, j])
    }
}
/// n = 10, i = 3, b < j, c < f, c < g, c < j, d < e, d < g, d < j, g < h, g < i
fn select_1262([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_1261([a, b, c, d, e, g, h, i, f, j])
    } else {
        select_1261([a, b, d, c, f, g, h, i, e, j])
    }
}
/// n = 11, i = 4, a < k, b < e, b < g, c < d, c < f, c < k, f < i, f < j, g < h, g < j, g < k
fn select_1263([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < g {
        select_1229([a, d, b, f, i, e, g, h, j])
    } else {
        select_1262([e, a, c, g, h, d, f, i, j, k])
    }
}
/// n = 12, i = 4, a < l, b < e, b < f, b < l, c < d, c < g, f < i, g < h, g < j, g < l, j < k
fn select_1264([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if j < f {
        select_1257([d, a, b, g, h, e, j, k, f, l])
    } else {
        select_1263([a, c, b, e, d, f, g, h, i, j, l])
    }
}
/// n = 14, i = 4, b < e, b < f, b < l, c < d, c < g, f < i, g < h, g < j, g < l, j < k, l < m, l < n
fn select_1265([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if a < l {
        select_1264([a, b, c, d, e, f, g, h, i, j, k, l])
    } else {
        select_537([b, c, d, e, f, g, h, i, j, k, l, a, m, n])
    }
}
/// n = 15, i = 5, a < f, b < e, b < h, c < d, c < g, c < k, g < j, g < m, h < i, h < k, h < m, k < l, m < n, m < o
fn select_1266([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < a {
        select_1265([d, g, b, e, j, a, h, i, f, k, l, m, n, o])
    } else {
        select_1251([a, c, b, e, d, f, h, i, g, j, k, l, m])
    }
}
/// n = 15, i = 5, a < h, b < g, b < l, c < f, c < k, c < o, d < e, d < i, i < j, i < k, i < l, k < n, l < m, l < o
fn select_1267([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if b < c {
        select_1252([a, d, b, g, e, h, c, i, j, f, l, m, k, n, o])
    } else {
        select_1266([a, d, c, f, e, h, b, i, j, g, k, n, l, m, o])
    }
}
/// n = 17, i = 5, a < h, b < g, c < f, c < m, c < o, d < e, d < i, i < j, i < k, i < m, k < l, k < o, m < n, o < p, o < q
fn select_1268([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if k < b {
        select_1192([e, a, c, i, j, f, h, k, l, b, m, g, n, o, p, q])
    } else {
        select_1267([a, b, c, d, e, f, g, h, i, j, m, k, l, n, o])
    }
}
/// n = 10, i = 3, c < f, c < j, d < e, d < f, e < j, f < g, f < h, f < i
fn select_1269([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_1133([b, e, c, a, f, g, h, i, j])
    } else {
        select_801([b, a, c, d, e, f, g, h, i])
    }
}
/// n = 10, i = 3, c < f, c < g, d < e, d < g, g < h, g < i, g < j
fn select_1270([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_1269([a, b, c, d, e, g, h, i, j, f])
    } else {
        select_1269([a, b, d, c, f, g, h, i, j, e])
    }
}
/// n = 12, i = 3, c < f, c < i, c < l, d < e, d < g, d < i, g < h, g < l, i < j, i < k
fn select_1271([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_1157([a, c, d, e, f, b, g, h, i, j, k, l])
    } else {
        select_1157([b, c, d, e, f, a, g, h, i, j, k, l])
    }
}
/// n = 13, i = 3, c < f, c < i, c < m, d < e, d < g, d < i, g < h, g < m, i < j, i < k, i < l
fn select_1272([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if j < g {
        select_1270([a, b, c, d, e, f, i, j, k, l])
    } else {
        select_1271([a, b, c, d, e, f, g, h, i, k, l, m])
    }
}
/// n = 14, i = 3, c < f, c < h, c < k, d < e, d < g, d < k, g < i, h < j, k < l, k < m, k < n
fn select_1273([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if g < h {
        select_1272([a, b, c, d, e, f, g, i, k, l, m, n, h])
    } else {
        select_1272([a, b, d, c, f, e, h, j, k, l, m, n, g])
    }
}
/// n = 11, i = 3, a < d, b < e, b < h, b < j, c < f, c < h, c < k, e < k, f < g, f < j, h < i
fn select_1274([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_576([f, b, g, e, h, a, i, k, d, j])
    } else {
        select_882([a, b, c, d, e, h, f, i, k, g])
    }
}
/// n = 11, i = 3, c < e, c < h, c < j, d < f, d < h, d < k, e < k, f < g, f < j, h < i
fn select_1275([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1274([a, c, d, b, e, f, g, h, i, j, k])
    } else {
        select_1274([b, c, d, a, e, f, g, h, i, j, k])
    }
}
/// n = 11, i = 2, a < j, a < k, b < d, b < f, b < i, c < e, c < i, c < j, c < k, e < g, f < h
fn select_1276([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < c {
        select_1045([a, d, f, c, e, i, h])
    } else {
        select_7([e, a, b, d, f, i, j, k, g])
    }
}
/// n = 7, i = 2, b < g, c < d, c < e, c < g, e < f
fn select_1277([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < a {
        select_316([d, b, e, a, f, g])
    } else {
        select_80([a, b, c, d, g, e])
    }
}
/// n = 11, i = 3, a < d, a < g, b < f, b < i, b < j, c < e, c < f, c < g, e < i, e < j, f < h, g < k
fn select_1278([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1277([d, b, c, e, g, k, f])
    } else {
        select_422([a, c, d, f, e, i, j, h, g])
    }
}
/// n = 12, i = 3, a < d, b < h, b < j, b < k, b < l, c < e, c < f, c < h, e < k, e < l, f < g, f < j, h < i
fn select_1279([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < a {
        select_1276([e, f, b, g, h, a, i, d, j, k, l])
    } else {
        select_1278([a, b, c, d, e, h, f, i, k, l, g])
    }
}
/// n = 12, i = 3, c < h, c < j, c < k, c < l, d < e, d < f, d < h, e < k, e < l, f < g, f < j, h < i
fn select_1280([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_1279([a, c, d, b, e, f, g, h, i, j, k, l])
    } else {
        select_1279([b, c, d, a, e, f, g, h, i, j, k, l])
    }
}
/// n = 12, i = 3, c < e, c < i, c < k, c < l, d < f, d < g, d < i, f < l, g < h, g < k, i < j
fn select_1281([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < f {
        select_1275([a, b, c, d, e, g, h, i, j, k, f])
    } else {
        select_1280([a, b, c, d, f, g, h, i, j, k, e, l])
    }
}
/// n = 10, i = 2, a < d, a < f, a < i, a < j, b < c, b < e, b < i, b < j, e < g, f < h
fn select_1282([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_153([a, b, c, d, e, g, i, j])
    } else {
        select_153([b, a, d, c, f, h, i, j])
    }
}
/// n = 11, i = 3, a < e, b < d, b < h, b < j, b < k, c < f, c < h, f < g, f < j, f < k, h < i
fn select_1283([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_1282([b, f, g, d, a, h, e, i, j, k])
    } else {
        select_517([a, b, c, d, e, h, f, i, g])
    }
}
/// n = 11, i = 3, c < e, c < h, c < j, c < k, d < f, d < h, f < g, f < j, f < k, h < i
fn select_1284([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1283([a, c, d, e, b, f, g, h, i, j, k])
    } else {
        select_1283([b, c, d, e, a, f, g, h, i, j, k])
    }
}
/// n = 10, i = 3, a < d, a < j, b < e, b < j, c < e, c < j, e < f, e < g, e < h, e < i
fn select_1285([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_22([a, f, g, h, i])
    } else {
        select_52([d, b, c, e, j])
    }
}
/// n = 12, i = 3, a < d, b < e, b < f, c < e, c < f, e < k, e < l, f < g, f < h, f < i, f < j
fn select_1286([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < a {
        select_214([e, f, g, h, i, j, a, k, l])
    } else {
        select_1285([a, b, c, d, f, g, h, i, j, e])
    }
}
/// n = 12, i = 3, a < e, b < f, b < g, c < d, c < f, c < g, f < l, g < h, g < i, g < j, g < k
fn select_1287([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if d < f {
        select_336([a, b, c, e, d, g, h, i, j, k, f])
    } else {
        select_1286([a, b, c, e, f, g, h, i, j, k, d, l])
    }
}
/// n = 12, i = 3, c < f, c < g, d < e, d < f, d < g, f < l, g < h, g < i, g < j, g < k
fn select_1288([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_1287([a, c, d, e, b, f, g, h, i, j, k, l])
    } else {
        select_1287([b, c, d, e, a, f, g, h, i, j, k, l])
    }
}
/// n = 14, i = 3, c < e, c < h, c < i, c < n, d < f, d < h, d < i, f < g, f < n, h < m, i < j, i < k, i < l
fn select_1289([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if f < i {
        select_1284([a, b, c, d, e, f, g, h, m, i, n])
    } else {
        select_1288([a, b, d, c, e, h, i, f, j, k, l, m])
    }
}
/// n = 14, i = 3, c < f, c < i, c < j, c < n, d < e, d < g, d < i, d < j, g < h, g < n, i < m, j < k, j < l
fn select_1290([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if e < j {
        select_1281([a, b, c, d, f, e, g, h, i, m, n, j])
    } else {
        select_1289([a, b, c, d, f, g, h, i, j, e, k, l, m, n])
    }
}
/// n = 15, i = 3, c < f, c < h, c < k, c < l, d < e, d < g, d < k, d < l, g < i, h < j, k < o, l < m, l < n
fn select_1291([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < h {
        select_1290([a, b, c, d, e, f, g, i, k, l, m, n, o, h])
    } else {
        select_1290([a, b, d, c, f, e, h, j, k, l, m, n, o, g])
    }
}
/// n = 17, i = 4, b < e, b < g, b < l, c < d, c < f, c < l, c < p, f < i, f < k, g < h, g < j, g < p, j < m, k < n, l < o, p < q
fn select_1292([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if f < g {
        select_1273([a, d, b, f, i, e, k, l, n, o, g, h, j, p])
    } else {
        select_1291([a, e, c, g, h, d, j, l, m, o, p, f, i, k, q])
    }
}
/// n = 7, i = 3, b < e, c < f, d < e, d < f, f < g
fn select_1293([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < b {
        select_256([a, b, d, f, g, e])
    } else {
        select_102([a, c, d, e, f])
    }
}
/// n = 8, i = 3, c < f, c < h, d < e, d < f, e < h, f < g
fn select_1294([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_397([b, e, c, a, f, g, h])
    } else {
        select_1293([b, a, c, d, e, f, g])
    }
}
/// n = 13, i = 3, c < f, c < g, c < m, d < e, d < f, d < g, e < m, f < l, g < h, g < i, g < j, g < k
fn select_1295([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if m < g {
        select_1294([a, b, c, d, e, f, l, m])
    } else {
        select_1288([a, b, c, d, e, f, g, h, i, j, k, l])
    }
}
/// n = 13, i = 3, c < f, c < g, c < h, d < e, d < g, d < h, g < m, h < i, h < j, h < k, h < l
fn select_1296([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if e < f {
        select_1295([a, b, c, d, e, g, h, i, j, k, l, m, f])
    } else {
        select_1295([a, b, d, c, f, g, h, i, j, k, l, m, e])
    }
}
/// n = 10, i = 2, b < e, b < g, b < j, c < d, c < f, c < j, f < h, g < i
fn select_1297([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < c {
        select_566([a, e, g, c, d, f, j, i])
    } else {
        select_566([a, d, f, b, e, g, j, h])
    }
}
/// n = 11, i = 3, a < f, b < e, b < i, b < k, c < d, c < g, c < i, g < h, g < k, i < j
fn select_1298([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_1297([d, b, g, h, e, a, i, f, j, k])
    } else {
        select_822([a, b, c, d, e, f, i, g, j, h])
    }
}
/// n = 11, i = 3, c < f, c < i, c < k, d < e, d < g, d < i, g < h, g < k, i < j
fn select_1299([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1298([a, c, d, e, f, b, g, h, i, j, k])
    } else {
        select_1298([b, c, d, e, f, a, g, h, i, j, k])
    }
}
/// n = 7, i = 2, a < d, a < e, a < f, a < g, b < c, b < e, b < f, b < g
fn select_1300([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if c < d {
        select_18([c, a, e, f, g])
    } else {
        select_18([d, b, e, f, g])
    }
}
/// n = 9, i = 2, a < d, a < h, a < i, b < c, b < e, b < h, b < i, e < f, e < g
fn select_1301([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_18([c, e, a, f, g])
    } else {
        select_1300([a, b, c, d, e, h, i])
    }
}
/// n = 8, i = 3, a < d, b < e, b < f, c < e, c < f, f < g, f < h
fn select_1302([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < a {
        select_18([e, f, a, g, h])
    } else {
        select_45([b, c, a, d, e, f])
    }
}
/// n = 8, i = 3, a < e, b < f, b < g, c < d, c < f, c < g, g < h
fn select_1303([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < g {
        select_114([a, b, c, e, d, f, g])
    } else {
        select_1302([a, b, c, e, f, g, d, h])
    }
}
/// n = 10, i = 3, a < e, a < h, b < d, b < i, b < j, c < f, c < h, f < g, f < i, f < j
fn select_1304([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_1301([b, f, g, d, a, e, h, i, j])
    } else {
        select_1303([b, c, a, e, d, h, f, g])
    }
}
/// n = 11, i = 4, a < f, b < e, b < i, b < j, c < g, c < k, d < f, d < g, f < k, g < h, g < i, g < j
fn select_1305([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_153([b, g, h, e, a, f, i, j])
    } else {
        select_289([b, c, a, d, e, f, g, h, k])
    }
}
/// n = 11, i = 4, b < e, b < j, b < k, c < g, c < i, d < f, d < g, f < i, g < h, g < j, g < k
fn select_1306([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_1304([f, b, c, e, a, g, h, i, j, k])
    } else {
        select_1305([a, b, c, d, e, f, g, h, j, k, i])
    }
}
/// n = 11, i = 4, b < g, b < j, b < k, c < f, c < h, d < e, d < h, h < i, h < j, h < k
fn select_1307([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_1306([a, b, c, d, g, e, h, i, f, j, k])
    } else {
        select_1306([a, b, d, c, g, f, h, i, e, j, k])
    }
}
/// n = 12, i = 4, b < g, b < l, c < f, c < j, c < l, d < e, d < h, h < i, h < j, h < l, j < k
fn select_1308([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < b {
        select_1299([a, e, c, h, i, f, b, g, j, k, l])
    } else {
        select_1307([a, c, b, d, e, g, f, h, i, j, l])
    }
}
/// n = 15, i = 4, b < g, c < f, c < j, c < k, d < e, d < h, h < i, h < j, h < k, j < o, k < l, k < m, k < n
fn select_1309([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if k < b {
        select_1296([a, e, c, h, i, f, j, k, b, l, m, n, o])
    } else {
        select_1308([a, b, c, d, e, f, g, h, i, j, o, k])
    }
}
/// n = 8, i = 2, a < g, a < h, b < e, b < f, b < h, c < d, c < f, c < g
fn select_1310([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < c {
        select_316([e, a, c, d, f, h])
    } else {
        select_316([d, a, b, e, f, g])
    }
}
/// n = 10, i = 3, a < c, a < e, a < j, b < d, b < f, d < i, e < h, f < g, f < i, f < j
fn select_1311([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_1310([d, a, f, g, c, j, i, e])
    } else {
        select_250([b, a, c, e, f, h, g, j, d])
    }
}
/// n = 10, i = 3, a < e, a < j, b < c, b < d, b < i, c < j, d < f, e < g, e < i, g < h
fn select_1312([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_79([c, a, d, f, e, j])
    } else {
        select_86([b, e, g, c, h, j, d, i])
    }
}
/// n = 8, i = 2, a < g, a < h, b < f, b < g, b < h, c < d, c < f, d < e
fn select_1313([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_27([b, d, a, e, f])
    } else {
        select_426([c, a, b, g, h, f, d])
    }
}
/// n = 10, i = 3, a < d, a < i, a < j, b < c, b < e, c < j, d < f, e < g, e < i, g < h
fn select_1314([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_1313([c, a, e, g, h, i, d, j])
    } else {
        select_708([a, b, d, e, f, g, h, i, c])
    }
}
/// n = 10, i = 3, a < d, a < e, a < j, b < c, b < f, e < g, f < h, f < j, h < i
fn select_1315([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < c {
        select_1312([b, a, d, e, f, g, h, i, j, c])
    } else {
        select_1314([a, b, c, e, f, g, h, i, j, d])
    }
}
/// n = 10, i = 3, a < g, a < j, b < e, b < i, b < j, c < d, c < f, c < j, f < h, g < i
fn select_1316([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_1311([c, a, d, g, f, b, e, h, i, j])
    } else {
        select_1315([c, b, e, d, f, a, h, g, i, j])
    }
}
/// n = 7, i = 2, b < e, c < d, c < f, f < g
fn select_1317([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < f {
        select_528([a, b, c, d, e, f])
    } else {
        select_20([b, c, d, e, f, a, g])
    }
}
/// n = 8, i = 2, b < g, c < f, c < h, d < e, d < h
fn select_1318([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < c {
        select_1317([a, d, b, g, e, c, f])
    } else {
        select_82([a, d, c, f, e, b, g, h])
    }
}
/// n = 10, i = 3, b < d, b < h, c < e, c < h, d < g, e < f, e < i, i < j
fn select_1319([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_103([a, c, d, g, h, e])
    } else {
        select_82([a, b, e, f, h, i, j, d])
    }
}
/// n = 11, i = 4, a < g, a < i, b < d, b < i, c < e, c < g, e < f, e < h, h < j, i < k
fn select_1320([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < b {
        select_1318([f, h, a, b, d, g, j, i])
    } else {
        select_1319([d, a, c, i, e, f, k, g, h, j])
    }
}
/// n = 12, i = 4, a < i, b < d, b < i, b < l, c < e, c < f, e < l, f < g, f < h, f < l, h < j, i < k
fn select_1321([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < a {
        select_1316([e, b, f, g, d, h, a, j, i, l])
    } else {
        select_1320([a, b, c, d, f, g, e, h, i, j, k])
    }
}
/// n = 8, i = 1, a < h, b < c, b < d, b < e, b < f, b < g
fn select_1322([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_2([b, h])
    } else {
        select_163([a, c, d, e, f, g])
    }
}
/// n = 11, i = 2, a < c, a < k, b < d, b < k, c < j, d < e, d < f, d < g, d < h, d < i
fn select_1323([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_163([a, e, f, g, h, i])
    } else {
        select_27([c, b, d, k, j])
    }
}
/// n = 11, i = 2, a < d, b < c, b < e, d < k, e < f, e < g, e < h, e < i, e < j
fn select_1324([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < a {
        select_1322([c, e, f, g, h, i, j, a])
    } else {
        select_1323([a, b, d, e, f, g, h, i, j, k, c])
    }
}
/// n = 11, i = 2, b < e, c < d, c < f, f < g, f < h, f < i, f < j, f < k
fn select_1325([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1324([a, c, d, b, f, g, h, i, j, k, e])
    } else {
        select_489([b, c, d, a, e, f, g, h, i, j, k])
    }
}
/// n = 6, i = 2, b < f, c < d, c < e
fn select_1326([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < d {
        select_528([a, b, c, e, f, d])
    } else {
        select_62([b, c, e, f, d, a])
    }
}
/// n = 6, i = 3, a < f, b < f, c < d, d < e
fn select_1327([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < d {
        select_84([b, c, f, d, e])
    } else {
        select_83([a, b, e])
    }
}
/// n = 10, i = 4, a < e, a < g, a < j, b < e, b < h, b < j, c < d, d < g, d < h, d < j, e < f, h < i
fn select_1328([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < e {
        select_90([a, b, g, h, i, j])
    } else {
        select_277([c, b, e, d, g, f, j])
    }
}
/// n = 10, i = 4, a < e, b < d, b < f, b < j, c < f, c < h, c < j, e < h, e < j, f < g, h < i
fn select_1329([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_1327([a, d, c, f, g, e])
    } else {
        select_1328([b, c, a, e, f, g, d, h, i, j])
    }
}
/// n = 11, i = 4, a < d, a < g, a < k, b < g, b < i, b < k, c < e, e < f, e < i, e < k, g < h, i < j
fn select_1330([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < g {
        select_257([a, b, e, f, d, i, j, k])
    } else {
        select_1329([c, a, b, d, e, g, h, i, j, k])
    }
}
/// n = 11, i = 4, a < h, a < k, b < d, b < h, b < k, c < e, e < f, e < g, e < k, g < i, h < j
fn select_1331([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_1326([f, b, g, a, i, d])
    } else {
        select_1330([b, a, c, d, e, f, h, j, g, i, k])
    }
}
/// n = 15, i = 4, a < h, b < d, b < h, b < k, c < e, e < f, e < g, e < k, g < i, h < j, k < l, k < m, k < n, k < o
fn select_1332([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if k < a {
        select_1325([f, g, b, d, i, k, a, l, m, n, o])
    } else {
        select_1331([a, b, c, d, e, f, g, h, i, j, k])
    }
}
/// n = 15, i = 4, a < i, b < e, b < i, b < l, c < d, c < f, f < g, f < h, f < l, h < j, i < k, l < m, l < n, l < o
fn select_1333([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if d < l {
        select_1321([a, b, c, e, d, f, g, h, i, j, k, l])
    } else {
        select_1332([a, b, c, e, f, g, h, i, j, k, l, d, m, n, o])
    }
}
/// n = 10, i = 3, a < d, b < f, b < j, c < e, c < f, e < j, f < g, f < h, f < i
fn select_1334([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_23([e, f, a, g, h, i, j])
    } else {
        select_93([b, a, c, d, e, j, f])
    }
}
/// n = 10, i = 3, a < f, b < e, b < g, c < d, c < g, g < h, g < i, g < j
fn select_1335([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < e {
        select_1334([a, b, c, f, d, g, h, i, j, e])
    } else {
        select_1334([a, c, b, f, e, g, h, i, j, d])
    }
}
/// n = 7, i = 3, a < f, a < g, b < e, b < g, c < e, c < f, d < e, d < f, d < g
fn select_1336([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < b {
        select_92([b, c, d, f, g])
    } else {
        select_92([a, c, d, e, g])
    }
}
/// n = 8, i = 4, a < g, a < h, b < f, b < h, c < f, c < g, c < h, d < e, d < h, e < g
fn select_1337([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_1336([a, b, e, c, f, g, h])
    } else {
        select_92([a, f, d, e, h])
    }
}
/// n = 8, i = 4, a < g, a < h, b < f, b < h, c < e, c < h, d < f, d < g, d < h
fn select_1338([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_1337([b, a, d, c, e, g, f, h])
    } else {
        select_93([c, a, b, g, f, e, h])
    }
}
/// n = 11, i = 4, a < g, b < f, b < h, c < e, c < h, d < f, d < g, d < h, h < i, h < j, h < k
fn select_1339([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < a {
        select_541([e, f, h, a, i, j, k])
    } else {
        select_1338([a, b, c, d, e, f, g, h])
    }
}
/// n = 11, i = 4, b < g, b < h, c < f, c < h, d < e, d < g, d < h, h < i, h < j, h < k
fn select_1340([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_1335([e, b, c, f, g, a, h, i, j, k])
    } else {
        select_1339([a, b, c, d, f, g, e, h, i, j, k])
    }
}
/// n = 16, i = 5, a < e, a < f, a < m, b < h, b < j, c < d, c < h, f < g, f < j, h < i, h < k, h < m, k < l, m < n, m < o, m < p
fn select_1341([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if h < f {
        select_1122([d, a, h, i, e, k, l, f, m, n, o, p, g, j])
    } else {
        select_1340([e, b, c, f, g, d, j, h, i, k, m])
    }
}
/// n = 16, i = 5, a < f, a < g, a < m, b < e, b < i, c < d, c < i, g < h, i < j, i < k, i < m, k < l, m < n, m < o, m < p
fn select_1342([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if d < g {
        select_1333([d, a, b, e, f, i, j, k, g, l, h, m, n, o, p])
    } else {
        select_1341([a, c, b, e, f, g, h, i, j, d, k, l, m, n, o, p])
    }
}
/// n = 17, i = 5, a < f, a < j, a < o, b < e, b < g, b < i, c < d, c < i, c < j, g < h, i < k, i < o, i < q, j < l, j < m, j < q, m < n, o < p
fn select_1343([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if i < j {
        select_1309([e, g, a, c, d, f, h, i, k, o, j, l, m, q, p])
    } else {
        select_1342([b, a, c, d, f, e, g, h, j, l, m, n, i, k, o, q])
    }
}
/// n = 18, i = 5, a < f, a < g, b < e, b < k, b < n, c < d, c < h, c < k, g < j, h < i, h < n, h < q, k < l, k < m, k < q, m < o, n < p, q < r
fn select_1344([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if h < a {
        select_1292([d, b, h, i, e, a, k, l, f, m, g, n, o, j, p, q, r])
    } else {
        select_1343([b, a, c, d, f, e, g, j, h, k, i, l, m, o, n, p, q])
    }
}
/// n = 18, i = 5, a < h, b < g, c < f, c < k, c < n, d < e, d < i, d < k, i < j, i < n, i < q, k < l, k < m, k < q, m < o, n < p, q < r
fn select_1345([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1344([a, c, d, e, f, h, b, i, j, g, k, l, m, n, o, p, q, r])
    } else {
        select_1344([b, c, d, e, f, g, a, i, j, h, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, a < h, b < g, c < f, c < l, c < p, d < e, d < i, d < l, i < j, i < k, i < p, k < m, l < n, l < o, o < q, p < r
fn select_1346([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if k < l {
        select_1268([a, b, c, d, e, f, g, h, i, j, k, m, p, r, l, n, o])
    } else {
        select_1345([a, b, c, d, e, f, g, h, i, j, l, n, o, p, q, r, k, m])
    }
}
/// n = 6, i = 3, b < f, c < e, d < e, d < f
fn select_1347([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if b < c {
        select_102([a, c, d, f, e])
    } else {
        select_102([a, b, d, e, f])
    }
}
/// n = 8, i = 4, a < h, b < g, c < f, d < e, d < h, e < g, f < h
fn select_1348([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < e {
        select_800([b, a, d, f, e, h])
    } else {
        select_1347([a, b, c, e, f, g])
    }
}
/// n = 7, i = 3, a < f, a < g, b < e, c < d, c < f, e < g
fn select_1349([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < d {
        select_95([a, c, b, e, f, d, g])
    } else {
        select_104([b, d, a, f, e])
    }
}
/// n = 8, i = 3, a < g, a < h, b < e, c < d, c < f, d < h, e < f, e < g
fn select_1350([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_90([c, e, d, a, g, f])
    } else {
        select_311([b, c, a, d, e, g, h])
    }
}
/// n = 8, i = 3, a < h, b < f, c < f, c < g, d < e, e < g, e < h
fn select_1351([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < a {
        select_1349([c, d, b, a, e, f, g])
    } else {
        select_1350([c, d, a, b, e, h, g, f])
    }
}
/// n = 9, i = 4, a < e, b < h, b < i, c < g, d < f, d < g, f < h, g < i
fn select_1352([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < g {
        select_1348([c, b, a, d, f, e, h, g])
    } else {
        select_1351([a, f, b, c, g, h, i, e])
    }
}
/// n = 8, i = 3, a < h, b < d, b < f, c < e, c < g, d < g, e < f, e < h
fn select_1353([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < a {
        select_90([d, c, a, e, f, g])
    } else {
        select_95([a, b, c, e, d, f, h])
    }
}
/// n = 9, i = 4, a < h, b < f, c < f, c < g, d < e, d < i, e < g, e < h, f < i
fn select_1354([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < b {
        select_528([b, a, c, g, h, f])
    } else {
        select_1353([a, c, d, f, e, g, i, h])
    }
}
/// n = 8, i = 4, a < g, a < h, b < f, c < f, d < e, e < g, f < h
fn select_1355([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_773([b, c, a, e, g, f])
    } else {
        select_92([a, d, f, e, h])
    }
}
/// n = 9, i = 4, a < e, b < g, c < g, c < h, d < f, d < i, f < h, g < i
fn select_1356([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < e {
        select_1354([a, b, c, d, f, g, h, e, i])
    } else {
        select_1355([d, b, c, a, e, g, f, i])
    }
}
/// n = 9, i = 4, a < g, b < h, c < f, c < i, d < e, d < h, h < i
fn select_1357([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < f {
        select_1352([a, c, b, d, g, e, h, f, i])
    } else {
        select_1356([a, b, d, c, g, f, h, e, i])
    }
}
/// n = 8, i = 3, a < g, a < h, b < d, b < f, c < e, e < f, e < g, e < h
fn select_1358([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_242([b, e, d, a, g, h, f])
    } else {
        select_446([b, a, c, d, e, g, h])
    }
}
/// n = 8, i = 3, b < h, c < f, c < g, d < e, e < f, e < g, e < h
fn select_1359([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < b {
        select_409([a, c, d, b, e, f, g])
    } else {
        select_1358([c, b, d, a, e, h, f, g])
    }
}
/// n = 8, i = 3, b < e, c < g, c < h, d < f, f < g, f < h
fn select_1360([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_919([a, c, d, b, e, f])
    } else {
        select_1359([a, b, c, d, f, g, h, e])
    }
}
/// n = 7, i = 4, a < f, a < g, b < e, c < d, c < f, e < g
fn select_1361([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < d {
        select_65([a, c, e, d, g, f])
    } else {
        select_71([b, d, a, f, e])
    }
}
/// n = 9, i = 4, a < d, b < f, c < e, c < g, e < h, e < i, f < g, f < h, f < i
fn select_1362([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_238([b, e, a, f, g, d, h, i])
    } else {
        select_1361([c, b, a, d, f, e, g])
    }
}
/// n = 6, i = 3, b < f, c < f, d < e
fn select_1363([a, b, c, d, e, f]: [usize; 6]) -> usize {
    if a < b {
        select_406([c, d, a, e, b, f])
    } else {
        select_105([c, d, b, a, e, f])
    }
}
/// n = 9, i = 4, a < e, b < g, c < d, c < f, f < h, f < i, g < h, g < i
fn select_1364([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < d {
        select_1362([a, b, c, e, f, g, d, h, i])
    } else {
        select_1363([f, b, d, a, e, g])
    }
}
/// n = 10, i = 4, a < e, b < f, b < i, c < d, c < g, f < j, g < h, g < j, h < i
fn select_1365([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < f {
        select_1360([d, a, b, g, e, h, f, i])
    } else {
        select_1364([a, b, c, d, e, g, f, h, j])
    }
}
/// n = 10, i = 4, a < j, b < f, c < g, c < j, d < e, d < h, g < i, h < i, h < j
fn select_1366([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < h {
        select_1357([b, a, c, d, e, g, f, h, j])
    } else {
        select_1365([b, c, d, e, f, g, h, a, j, i])
    }
}
/// n = 8, i = 3, b < d, b < g, c < e, c < h, d < h, e < f, e < g
fn select_1367([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < d {
        select_1178([a, b, c, e, f, d, g])
    } else {
        select_235([b, c, e, d, f, a, h, g])
    }
}
/// n = 8, i = 4, a < g, b < e, b < h, c < d, c < g, e < f, g < h
fn select_1368([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < g {
        select_255([a, c, e, f, d, g])
    } else {
        select_52([d, b, g, e, h])
    }
}
/// n = 9, i = 4, a < i, b < f, b < i, c < d, c < e, e < h, e < i, f < g, f < h
fn select_1369([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < a {
        select_1367([d, e, b, a, f, g, h, i])
    } else {
        select_1368([a, b, c, d, f, g, e, i])
    }
}
/// n = 9, i = 3, a < e, a < g, a < i, b < c, b < d, b < g, d < i, e < f, g < h
fn select_1370([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < d {
        select_39([e, b, c, f, g, h, d])
    } else {
        select_396([c, d, a, g, h, e, i])
    }
}
/// n = 10, i = 4, a < f, a < h, b < f, b < h, c < d, c < h, c < j, d < e, f < g, f < j, h < i
fn select_1371([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < d {
        select_150([f, c, g, h, i, d, j])
    } else {
        select_248([d, a, b, e, h, i, f])
    }
}
/// n = 11, i = 4, a < i, b < e, b < i, c < d, c < h, c < i, d < g, e < f, e < h, h < j, i < k
fn select_1372([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_1370([c, e, f, a, d, g, h, j, i])
    } else {
        select_1371([a, b, c, d, g, e, f, i, k, h])
    }
}
/// n = 11, i = 4, a < e, b < i, c < h, c < i, d < f, d < i, f < g, f < h, h < j, i < k
fn select_1373([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < c {
        select_1369([b, d, a, e, c, f, g, h, i])
    } else {
        select_1372([b, d, c, a, f, g, e, h, i, j, k])
    }
}
/// n = 8, i = 4, a < e, a < f, b < f, b < g, c < f, c < g, d < e, d < g, g < h
fn select_1374([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if g < e {
        select_84([a, d, f, g, h])
    } else {
        select_71([b, c, d, e, f])
    }
}
/// n = 8, i = 4, a < g, b < e, b < f, c < f, c < g, d < f, d < g, g < h
fn select_1375([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_1374([b, c, d, a, e, f, g, h])
    } else {
        select_71([c, d, e, a, f])
    }
}
/// n = 10, i = 4, a < e, b < g, b < i, b < j, c < f, c < g, d < f, d < g, f < i, f < j, g < h
fn select_1376([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_86([b, f, a, g, e, h, i, j])
    } else {
        select_1375([b, a, c, d, e, f, g, h])
    }
}
/// n = 10, i = 4, a < e, b < g, b < h, c < f, c < h, c < j, d < f, d < g, d < h, g < j, h < i
fn select_1377([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < g {
        select_289([a, b, c, d, e, f, h, i, g])
    } else {
        select_1376([a, c, b, d, e, g, h, i, f, j])
    }
}
/// n = 12, i = 5, a < e, b < h, b < i, b < j, c < f, c < i, d < g, d < j, f < j, g < h, g < i, i < k, j < l
fn select_1378([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < g {
        select_1376([a, b, d, f, e, g, j, l, h, i])
    } else {
        select_1377([a, c, b, g, e, h, f, i, k, j])
    }
}
/// n = 12, i = 5, a < e, b < f, b < k, c < h, c < j, c < k, d < g, d < h, f < j, g < k, h < i, k < l
fn select_1379([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < f {
        select_1373([a, g, b, c, e, h, i, f, k, j, l])
    } else {
        select_1378([a, c, d, b, e, g, f, j, h, k, i, l])
    }
}
/// n = 12, i = 5, a < e, b < j, b < k, c < g, c < k, d < f, d < h, f < i, g < j, h < k, k < l
fn select_1380([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < b {
        select_1366([h, a, c, f, i, e, g, b, j, k])
    } else {
        select_1379([a, c, b, d, e, g, h, f, i, j, k, l])
    }
}
/// n = 12, i = 5, a < g, b < f, b < k, c < e, c < k, d < h, d < i, h < j, i < k, k < l
fn select_1381([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < f {
        select_1380([a, b, c, d, g, h, e, i, j, f, k, l])
    } else {
        select_1380([a, c, b, d, g, h, f, i, j, e, k, l])
    }
}
/// n = 8, i = 3, a < d, b < e, b < f, c < e, c < f, e < h, f < g
fn select_1382([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_27([f, e, a, h, g])
    } else {
        select_248([a, b, c, d, f, g, e])
    }
}
/// n = 8, i = 3, a < f, b < d, b < g, c < e, c < f, e < g, f < h
fn select_1383([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < d {
        select_131([b, e, a, f, h, g])
    } else {
        select_271([a, c, b, d, e, g])
    }
}
/// n = 10, i = 4, a < d, a < j, b < f, c < e, c < h, e < g, f < h, g < j, h < i
fn select_1384([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_1382([a, c, f, d, e, h, i, g])
    } else {
        select_1383([b, a, e, d, g, f, j, h])
    }
}
/// n = 10, i = 4, a < h, b < h, c < e, c < i, d < f, d < h, f < g, g < i, h < j
fn select_1385([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_1384([c, a, d, e, f, b, g, h, j, i])
    } else {
        select_1384([c, b, d, e, f, a, g, h, j, i])
    }
}
/// n = 8, i = 4, a < g, a < h, b < f, b < h, c < f, c < h, d < e, d < h, e < g
fn select_1386([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < e {
        select_93([a, c, d, f, e, g, h])
    } else {
        select_104([b, c, a, g, f])
    }
}
/// n = 10, i = 4, a < g, b < f, b < h, c < f, c < h, d < e, d < h, e < g, h < i, h < j
fn select_1387([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < a {
        select_212([e, f, h, a, i, j])
    } else {
        select_1386([a, b, c, d, e, f, g, h])
    }
}
/// n = 7, i = 2, a < g, b < d, c < e, c < g, e < f
fn select_1388([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if b < a {
        select_85([c, b, a, d, e, f])
    } else {
        select_137([a, c, e, b, f, d, g])
    }
}
/// n = 10, i = 3, a < e, b < f, b < j, c < d, c < f, c < i, e < i, e < j, f < g, f < h
fn select_1389([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_686([a, d, b, f, g, h])
    } else {
        select_405([b, c, a, d, e, i, j])
    }
}
/// n = 12, i = 4, a < g, a < i, b < f, b < i, c < e, d < f, d < h, d < i, e < g, e < h, h < j, i < k, i < l
fn select_1390([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < b {
        select_1388([b, a, d, g, h, j, f])
    } else {
        select_1389([c, a, d, f, e, i, k, l, h, g])
    }
}
/// n = 12, i = 4, a < f, b < g, b < i, c < e, c < i, d < g, d < h, d < i, f < h, h < l, i < j, i < k
fn select_1391([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < f {
        select_1387([a, b, d, c, e, g, f, i, j, k])
    } else {
        select_1390([c, b, a, d, f, g, e, h, i, l, j, k])
    }
}
/// n = 12, i = 4, a < h, b < h, c < g, c < i, d < f, d < i, e < g, e < h, e < i, h < l, i < j, i < k
fn select_1392([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_1391([a, c, d, e, f, b, g, h, i, j, k, l])
    } else {
        select_1391([b, c, d, e, f, a, g, h, i, j, k, l])
    }
}
/// n = 12, i = 4, a < h, b < h, c < i, d < g, d < i, e < f, e < h, e < i, h < l, i < j, i < k
fn select_1393([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < c {
        select_1385([a, b, d, e, g, f, c, h, i, l])
    } else {
        select_1392([a, b, c, d, e, g, f, h, i, j, k, l])
    }
}
/// n = 8, i = 4, a < g, a < h, b < f, b < h, c < d, c < e, e < h, f < g
fn select_1394([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < d {
        select_620([a, f, c, e, d, g, h])
    } else {
        select_773([a, e, d, b, f, h])
    }
}
/// n = 10, i = 4, a < g, a < h, b < d, b < h, c < e, c < h, d < g, e < f, h < i, h < j
fn select_1395([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < e {
        select_418([d, c, g, h, e, i, j])
    } else {
        select_369([a, c, b, d, e, f, g, h])
    }
}
/// n = 10, i = 4, a < e, b < h, c < g, c < h, d < f, d < h, f < g, h < i, h < j
fn select_1396([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if a < b {
        select_1394([c, d, a, e, b, f, g, h])
    } else {
        select_1395([c, d, b, f, a, e, g, h, i, j])
    }
}
/// n = 10, i = 3, a < e, a < g, b < d, b < e, b < f, c < d, c < f, c < g, f < h, g < i, g < j
fn select_1397([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < g {
        select_62([a, c, d, e, f, h])
    } else {
        select_1196([b, a, c, d, e, g, i, j])
    }
}
/// n = 10, i = 3, a < g, a < h, b < f, b < h, c < d, c < f, c < g, d < e, h < i, h < j
fn select_1398([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_62([b, d, e, f, a, g])
    } else {
        select_1397([b, c, a, g, f, d, h, e, i, j])
    }
}
/// n = 10, i = 4, a < d, a < f, b < f, b < g, c < e, c < j, e < g, f < j, g < h, g < i
fn select_1399([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_52([d, c, f, e, j])
    } else {
        select_265([a, b, e, d, g, h, i, f])
    }
}
/// n = 11, i = 4, a < g, a < i, b < g, b < h, c < e, c < f, d < f, d < g, f < h, f < i, g < j, g < k
fn select_1400([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1399([c, d, a, e, b, f, g, j, k, i])
    } else {
        select_1399([c, d, b, e, a, f, g, j, k, h])
    }
}
/// n = 11, i = 4, a < e, b < h, b < i, c < g, c < i, d < f, d < i, f < g, f < h, i < j, i < k
fn select_1401([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_1398([b, c, f, a, e, g, h, i, j, k])
    } else {
        select_1400([b, c, a, d, e, f, i, g, h, j, k])
    }
}
/// n = 11, i = 4, a < f, b < h, b < i, c < e, c < i, d < g, d < i, g < h, i < j, i < k
fn select_1402([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < g {
        select_1396([a, b, d, c, f, e, g, i, j, k])
    } else {
        select_1401([a, b, c, d, f, g, e, h, i, j, k])
    }
}
/// n = 11, i = 4, a < h, b < g, b < i, c < f, c < i, d < e, d < i, i < j, i < k
fn select_1403([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_1402([a, c, b, d, g, h, e, f, i, j, k])
    } else {
        select_1402([a, d, b, c, g, h, f, e, i, j, k])
    }
}
/// n = 9, i = 4, a < e, a < i, b < e, b < g, b < h, c < f, c < g, d < f, d < g, f < h, f < i
fn select_1404([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_90([b, f, g, a, i, h])
    } else {
        select_1374([b, c, d, a, e, g, f, i])
    }
}
/// n = 10, i = 5, a < h, a < j, b < f, b < g, c < f, c < g, d < e, d < j, e < h, e < i, g < i, g < j
fn select_1405([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_1404([a, e, b, c, h, g, f, i, j])
    } else {
        select_773([a, g, f, d, e, j])
    }
}
/// n = 9, i = 3, a < f, b < d, b < e, c < e, c < f, e < g, f < h, f < i
fn select_1406([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < f {
        select_550([a, d, c, e, g])
    } else {
        select_310([b, a, e, f, h, i, g])
    }
}
/// n = 11, i = 4, a < h, a < i, b < e, b < i, c < d, c < g, c < i, d < f, e < g, e < h, i < j, i < k
fn select_1407([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_1406([a, d, b, f, e, i, g, j, k])
    } else {
        select_1397([a, e, c, g, h, d, i, f, j, k])
    }
}
/// n = 12, i = 5, a < g, b < h, b < j, c < f, c < g, d < e, d < j, e < h, e < i, f < i, f < j, j < k, j < l
fn select_1408([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < f {
        select_1405([b, a, c, d, e, g, f, h, i, j])
    } else {
        select_1407([b, d, f, a, e, g, i, h, j, k, l])
    }
}
/// n = 12, i = 5, a < h, b < i, b < j, c < e, c < j, d < f, d < h, e < i, f < g, f < j, j < k, j < l
fn select_1409([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if g < e {
        select_1396([a, b, c, f, h, g, e, j, k, l])
    } else {
        select_1408([a, b, d, c, e, f, h, i, g, j, k, l])
    }
}
/// n = 12, i = 5, a < i, b < f, b < j, c < e, c < j, d < g, d < i, g < h, g < j, j < k, j < l
fn select_1410([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < f {
        select_1409([a, b, c, d, e, g, h, i, f, j, k, l])
    } else {
        select_1409([a, c, b, d, f, g, h, i, e, j, k, l])
    }
}
/// n = 12, i = 5, b < g, b < j, c < f, c < j, d < e, d < h, h < i, h < j, j < k, j < l
fn select_1411([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < a {
        select_1403([e, b, c, h, i, f, g, a, j, k, l])
    } else {
        select_1410([a, b, c, d, f, g, h, i, e, j, k, l])
    }
}
/// n = 14, i = 5, a < j, b < f, b < k, c < e, c < j, c < k, d < g, d < h, g < j, h < i, h < k, j < n, k < l, k < m
fn select_1412([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if j < f {
        select_1393([a, g, b, h, c, e, i, j, k, l, m, n])
    } else {
        select_1411([a, b, c, d, g, e, f, h, i, k, l, m])
    }
}
/// n = 15, i = 5, a < g, a < k, b < f, b < l, c < e, c < k, c < l, d < h, d < i, h < k, i < j, i < l, k < o, l < m, l < n
fn select_1413([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if g < l {
        select_1381([b, a, c, d, e, g, f, i, h, j, k, o])
    } else {
        select_1412([a, b, c, d, e, f, h, i, j, k, l, m, n, o])
    }
}
/// n = 9, i = 3, a < d, a < i, b < f, b < g, c < e, c < f, c < g, e < i, g < h
fn select_1414([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < g {
        select_891([b, a, c, d, e, f, i, g])
    } else {
        select_1302([a, b, c, d, f, g, e, h])
    }
}
/// n = 10, i = 3, a < f, a < g, b < d, b < e, c < f, c < g, c < h, c < i, e < h, e < i, g < j
fn select_1415([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_260([d, c, e, a, h, i])
    } else {
        select_67([b, c, a, d, f, e, g, j])
    }
}
/// n = 10, i = 3, a < g, a < h, b < e, b < f, c < d, c < g, c < h, c < i, f < i, h < j
fn select_1416([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < f {
        select_1414([b, a, c, e, d, g, h, j, f])
    } else {
        select_1415([a, b, c, e, f, g, h, d, i, j])
    }
}
/// n = 8, i = 2, a < g, a < h, b < d, b < h, c < e, c < g, e < f
fn select_1417([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if b < c {
        select_42([d, a, c, e, h])
    } else {
        select_1208([a, b, e, f, d, g])
    }
}
/// n = 9, i = 2, a < i, b < f, b < i, c < d, c < e, e < g, f < h
fn select_1418([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < e {
        select_1417([a, c, b, d, f, h, i, e])
    } else {
        select_631([b, c, d, f, e, a, g, h])
    }
}
/// n = 11, i = 3, a < f, a < h, b < d, b < g, c < f, c < g, c < h, c < j, d < e, d < j, g < i, h < k
fn select_1419([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_423([c, d, a, e, g, i, j])
    } else {
        select_817([b, a, c, f, h, g, d, k, i, e])
    }
}
/// n = 11, i = 3, a < g, a < i, b < e, b < h, c < d, c < g, c < h, c < i, e < f, h < j, i < k
fn select_1420([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_1418([d, b, a, g, i, h, k, j, e])
    } else {
        select_1419([a, b, c, e, f, g, h, i, j, d, k])
    }
}
/// n = 11, i = 3, a < f, b < i, c < g, c < h, d < e, d < g, d < h, d < i, h < j, i < k
fn select_1421([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1416([c, a, d, e, f, b, g, h, i, j])
    } else {
        select_1420([c, b, d, e, a, f, g, i, h, k, j])
    }
}
/// n = 11, i = 3, c < i, d < g, d < h, e < f, e < g, e < h, e < i, h < j, i < k
fn select_1422([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1421([a, c, d, e, f, b, g, h, i, j, k])
    } else {
        select_1421([b, c, d, e, f, a, g, h, i, j, k])
    }
}
/// n = 8, i = 3, a < e, a < h, b < e, b < f, c < d, c < f, d < h, f < g
fn select_1423([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < d {
        select_237([a, c, e, f, d, g])
    } else {
        select_95([a, b, c, d, e, f, h])
    }
}
/// n = 9, i = 3, a < f, a < i, b < e, b < f, b < g, c < d, c < e, d < g, d < i, f < h
fn select_1424([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_90([b, d, e, a, i, g])
    } else {
        select_872([b, c, a, e, d, f, i, h])
    }
}
/// n = 9, i = 3, a < e, a < f, b < d, b < g, c < f, c < g, c < i, e < i, g < h
fn select_1425([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_1423([a, c, b, d, f, g, h, e])
    } else {
        select_1424([b, c, a, e, f, g, i, h, d])
    }
}
/// n = 10, i = 3, a < g, a < j, b < e, b < f, c < d, c < g, c < h, e < j, f < h, g < i
fn select_1426([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < a {
        select_103([e, c, f, a, d, h])
    } else {
        select_1425([b, c, a, d, e, f, g, i, j])
    }
}
/// n = 11, i = 4, a < d, a < k, b < e, b < g, c < f, c < k, d < j, e < i, e < k, f < g, f < i, f < j, g < h
fn select_1427([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_888([a, b, e, g, d, h, i, j])
    } else {
        select_1353([d, b, c, e, f, g, k, j])
    }
}
/// n = 11, i = 4, a < e, a < k, b < d, b < h, c < f, c < k, d < k, e < j, f < g, f < h, f < j, h < i
fn select_1428([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < d {
        select_1078([a, b, f, g, e, h, i, d, j])
    } else {
        select_1427([a, b, c, e, d, f, h, i, g, j, k])
    }
}
/// n = 11, i = 4, a < e, a < h, b < d, b < i, c < f, c < h, e < k, f < g, f < i, f < k, i < j
fn select_1429([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if h < d {
        select_1426([b, a, f, g, h, e, i, k, j, d])
    } else {
        select_1428([a, b, c, d, e, f, g, i, j, k, h])
    }
}
/// n = 9, i = 3, a < f, a < i, b < d, b < g, c < e, c < f, c < g, e < i, g < h
fn select_1430([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if e < d {
        select_1417([e, a, b, f, g, h, d, i])
    } else {
        select_966([a, c, b, d, f, g, h, e])
    }
}
/// n = 10, i = 4, a < f, a < g, b < e, b < j, c < d, c < f, c < h, e < g, e < h, f < j, h < i
fn select_1431([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < f {
        select_695([a, e, c, d, g, h, i])
    } else {
        select_112([a, b, c, d, e, f, g, j])
    }
}
/// n = 11, i = 4, a < d, a < i, b < e, b < g, c < f, c < h, e < h, e < j, f < g, f < i, f < j, i < k
fn select_1432([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_51([c, e, a, f, g, d, h, j])
    } else {
        select_1431([b, c, a, d, f, e, g, i, k, h])
    }
}
/// n = 11, i = 4, a < e, a < h, b < d, b < j, c < f, c < i, e < i, f < g, f < h, f < j, j < k
fn select_1433([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < e {
        select_1430([a, b, f, d, g, h, j, k, e])
    } else {
        select_1432([b, a, c, d, e, f, h, i, j, g, k])
    }
}
/// n = 11, i = 4, a < i, b < h, c < e, c < j, d < f, d < h, f < g, f < i, f < j, j < k
fn select_1434([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if b < a {
        select_1429([b, c, d, e, a, f, g, h, j, k, i])
    } else {
        select_1433([a, c, d, e, b, f, g, i, h, j, k])
    }
}
/// n = 12, i = 5, a < j, b < g, b < k, c < f, c < h, d < e, d < h, h < i, h < j, h < k, k < l
fn select_1435([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < f {
        select_1434([a, e, b, c, g, h, i, f, j, k, l])
    } else {
        select_1434([a, f, b, d, g, h, i, e, j, k, l])
    }
}
/// n = 14, i = 5, a < j, a < l, b < g, b < k, c < f, c < h, d < e, d < h, h < i, h < j, h < k, h < l, k < m, l < n
fn select_1436([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if l < g {
        select_1422([e, f, b, a, h, i, j, l, k, n, m])
    } else {
        select_1435([a, b, c, d, e, f, g, h, i, j, k, m])
    }
}
/// n = 9, i = 4, a < e, a < i, b < e, b < g, b < h, c < f, d < f, f < g, f < h, f < i
fn select_1437([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_27([a, b, g, h, i])
    } else {
        select_287([b, c, d, e, f, i])
    }
}
/// n = 10, i = 5, a < h, a < j, b < f, c < f, d < e, d < j, e < h, e < i, f < g, f < i, f < j
fn select_1438([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < g {
        select_1437([a, e, b, c, h, f, g, i, j])
    } else {
        select_92([a, g, d, e, j])
    }
}
/// n = 8, i = 5, a < h, b < g, c < e, d < f, e < h, f < g
fn select_1439([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_406([b, a, d, h, f, g])
    } else {
        select_406([a, b, c, g, e, h])
    }
}
/// n = 10, i = 5, a < h, a < j, b < g, c < f, c < j, d < e, d < g, f < h, f < i, g < i, g < j
fn select_1440([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < e {
        select_1438([a, b, d, c, f, g, e, h, i, j])
    } else {
        select_1439([a, b, c, d, f, e, g, h])
    }
}
/// n = 12, i = 5, a < e, b < h, b < j, c < g, d < f, d < j, f < h, f < i, g < i, g < j, j < k, j < l
fn select_1441([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < g {
        select_1440([b, c, d, a, e, f, g, h, i, j])
    } else {
        select_1407([b, d, g, a, f, e, i, h, j, k, l])
    }
}
/// n = 12, i = 5, a < e, b < i, b < j, c < g, d < f, d < j, f < i, g < h, g < j, j < k, j < l
fn select_1442([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < f {
        select_1396([a, b, d, g, e, h, f, j, k, l])
    } else {
        select_1441([a, b, c, d, e, f, g, i, h, j, k, l])
    }
}
/// n = 12, i = 5, a < g, b < f, b < j, c < e, c < j, d < h, h < i, h < j, j < k, j < l
fn select_1443([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < f {
        select_1442([a, b, d, c, g, e, h, i, f, j, k, l])
    } else {
        select_1442([a, c, d, b, g, f, h, i, e, j, k, l])
    }
}
/// n = 15, i = 5, a < g, a < k, b < f, b < j, c < e, c < j, c < k, d < h, h < i, h < j, h < k, j < l, j < m, k < n, k < o
fn select_1444([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if j < k {
        select_1443([a, b, c, d, e, f, g, h, i, j, l, m])
    } else {
        select_1443([b, a, c, d, e, g, f, h, i, k, n, o])
    }
}
/// n = 17, i = 5, a < h, a < l, b < g, b < m, b < n, c < f, c < j, d < e, d < j, d < n, h < i, h < n, j < k, j < l, j < m, m < o, n < p, n < q
fn select_1445([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if j < h {
        select_1436([a, b, c, d, e, f, g, j, k, l, m, h, o, i])
    } else {
        select_1444([b, c, d, a, e, f, g, h, i, j, n, k, l, p, q])
    }
}
/// n = 17, i = 5, a < h, a < k, b < g, b < m, b < n, c < f, c < i, d < e, d < k, d < n, i < j, i < n, k < l, k < m, m < q, n < o, n < p
fn select_1446([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if f < k {
        select_1413([a, b, d, c, e, g, h, f, i, j, k, n, o, p, l])
    } else {
        select_1445([c, b, a, d, e, h, g, i, j, k, l, f, m, n, q, o, p])
    }
}
/// n = 8, i = 2, b < e, c < d, c < f, f < g, f < h
fn select_1447([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < b {
        select_212([a, d, f, b, g, h])
    } else {
        select_103([a, b, c, d, e, f])
    }
}
/// n = 9, i = 3, b < f, b < g, c < d, c < e, c < g, g < h, g < i
fn select_1448([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_1447([e, d, b, f, a, g, h, i])
    } else {
        select_928([a, b, c, e, f, d, g, h, i])
    }
}
/// n = 9, i = 2, a < f, b < e, c < d, c < g, g < h, g < i
fn select_1449([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_659([a, c, d, f, b, g, h, i, e])
    } else {
        select_659([b, c, d, e, a, g, h, i, f])
    }
}
/// n = 10, i = 3, a < g, b < d, b < h, c < e, c < g, c < h, e < f, h < i, h < j
fn select_1450([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_659([e, b, d, f, a, h, i, j, g])
    } else {
        select_47([a, b, c, d, g, e, h, i, j, f])
    }
}
/// n = 10, i = 3, b < e, b < h, c < d, c < f, c < h, f < g, h < i, h < j
fn select_1451([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < a {
        select_1449([d, f, b, e, g, a, h, i, j])
    } else {
        select_1450([a, b, c, e, f, g, d, h, i, j])
    }
}
/// n = 11, i = 4, a < d, a < e, b < c, b < f, e < h, e < i, f < g, f < j, j < k
fn select_1452([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_1448([d, b, e, h, i, c, f, g, j])
    } else {
        select_1451([c, a, f, g, d, j, k, e, h, i])
    }
}
/// n = 9, i = 3, a < d, a < e, b < d, b < f, c < e, c < f, e < i, f < g, f < h
fn select_1453([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_3([a, g, h])
    } else {
        select_90([b, c, d, e, i, f])
    }
}
/// n = 9, i = 3, a < e, a < g, b < f, b < g, c < d, c < e, c < f, f < h, g < i
fn select_1454([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < f {
        select_702([b, a, c, d, e, g, i, f])
    } else {
        select_1453([a, c, b, e, g, f, d, h, i])
    }
}
/// n = 10, i = 3, a < g, b < f, b < g, b < i, c < d, c < e, c < f, e < i, f < h, g < j
fn select_1455([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_397([d, e, b, a, f, h, i])
    } else {
        select_1454([a, b, c, d, e, f, g, h, j])
    }
}
/// n = 10, i = 3, a < g, b < d, b < f, b < i, c < e, c < f, c < g, e < i, f < h, g < j
fn select_1456([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < a {
        select_575([e, b, d, f, a, h, g, i])
    } else {
        select_696([a, b, c, d, e, f, g, h, j])
    }
}
/// n = 10, i = 3, a < h, b < e, b < f, b < g, c < d, c < g, c < h, g < i, h < j
fn select_1457([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < d {
        select_1455([a, c, b, f, e, g, h, i, d, j])
    } else {
        select_1456([a, b, c, f, d, g, h, i, e, j])
    }
}
/// n = 10, i = 3, a < c, a < d, a < h, b < e, b < h, e < f, e < g, h < i, h < j
fn select_1458([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < e {
        select_1061([c, d, b, h, e, i, j])
    } else {
        select_1050([a, b, c, d, e, f, g, h])
    }
}
/// n = 8, i = 3, a < c, a < d, a < h, b < e, b < f, e < h, f < g
fn select_1459([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if f < e {
        select_276([a, b, c, d, f, e, g])
    } else {
        select_1040([a, b, c, d, e, f, g, h])
    }
}
/// n = 8, i = 3, a < h, b < d, b < g, c < e, c < g, e < f, e < h
fn select_1460([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < a {
        select_981([b, e, f, d, g, a, h])
    } else {
        select_1258([b, a, c, d, g, e, f, h])
    }
}
/// n = 10, i = 4, a < e, a < i, b < c, b < d, c < j, d < f, d < i, e < g, e < h, e < j
fn select_1461([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < f {
        select_1459([e, b, g, h, c, d, i, j])
    } else {
        select_1460([c, d, a, f, e, h, i, j])
    }
}
/// n = 11, i = 4, a < e, a < i, b < c, b < d, b < j, d < f, d < i, e < g, e < h, e < j, j < k
fn select_1462([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if j < c {
        select_1458([e, b, g, h, d, f, i, j, c, k])
    } else {
        select_1461([a, b, c, d, e, f, g, h, i, j])
    }
}
/// n = 11, i = 4, a < d, a < e, a < j, b < c, b < f, e < i, f < g, f < h, f < j, j < k
fn select_1463([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if c < e {
        select_1457([c, f, a, d, g, h, j, e, k, i])
    } else {
        select_1462([b, a, d, e, f, i, g, h, c, j, k])
    }
}
/// n = 13, i = 4, a < d, a < f, b < c, b < e, b < l, e < g, e < j, f < h, f < i, f < l, j < k, l < m
fn select_1464([a, b, c, d, e, f, g, h, i, j, k, l, m]: [usize; 13]) -> usize {
    if j < l {
        select_1452([a, b, c, d, f, e, g, h, i, j, k])
    } else {
        select_1463([b, a, d, c, e, f, h, i, g, l, m])
    }
}
/// n = 8, i = 2, b < d, c < e, c < f, e < h, f < g
fn select_1465([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_1388([a, b, c, d, f, g, e])
    } else {
        select_632([b, c, d, f, e, a, h, g])
    }
}
/// n = 9, i = 2, b < d, c < e, c < f, e < i, f < g, f < h
fn select_1466([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < b {
        select_149([a, e, f, b, g, h, i])
    } else {
        select_397([a, b, c, d, e, i, f])
    }
}
/// n = 10, i = 2, b < e, c < f, d < g, f < j, g < h, g < i
fn select_1467([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if c < d {
        select_1465([a, b, c, e, d, f, j, g])
    } else {
        select_1466([a, b, d, e, c, g, h, i, f])
    }
}
/// n = 10, i = 3, a < d, a < e, a < j, b < f, b < j, c < e, c < f, c < j, f < g, f < h, f < i
fn select_1468([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if d < f {
        select_102([d, b, c, e, j])
    } else {
        select_12([a, b, e, f, g, h, i, j])
    }
}
/// n = 12, i = 3, a < d, a < e, a < l, b < f, b < g, b < l, c < e, c < f, c < g, c < l, f < j, f < k, g < h, g < i
fn select_1469([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < g {
        select_1468([a, b, c, d, e, f, g, j, k, l])
    } else {
        select_1468([a, b, c, d, e, g, f, h, i, l])
    }
}
/// n = 12, i = 3, a < d, a < h, a < l, b < i, b < l, c < e, c < h, c < i, c < l, e < f, e < g, i < j, i < k
fn select_1470([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < b {
        select_673([a, e, f, g, d, h, b, i])
    } else {
        select_1469([a, b, c, d, h, e, i, j, k, f, g, l])
    }
}
/// n = 9, i = 3, a < e, a < i, b < e, b < f, b < h, c < d, c < f, d < h, d < i, f < g
fn select_1471([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < a {
        select_137([b, d, a, f, i, g, h])
    } else {
        select_872([a, b, c, e, f, d, g, i])
    }
}
/// n = 9, i = 3, a < d, a < f, b < f, b < g, b < i, c < e, c < g, e < i, g < h
fn select_1472([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < e {
        select_702([c, b, a, d, f, g, h, e])
    } else {
        select_1471([a, b, c, e, f, g, h, i, d])
    }
}
/// n = 12, i = 3, a < g, b < e, b < f, b < k, c < h, c < k, d < f, d < g, d < h, d < k, g < l, h < i, h < j
fn select_1473([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < c {
        select_1472([b, d, a, e, c, f, g, l, h])
    } else {
        select_858([b, d, c, e, a, f, h, i, j, g, k])
    }
}
/// n = 12, i = 3, b < e, b < h, b < l, c < i, c < l, d < f, d < h, d < i, d < l, f < g, i < j, i < k
fn select_1474([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < a {
        select_1470([b, c, d, e, f, a, g, h, i, j, k, l])
    } else {
        select_1473([a, b, c, d, e, h, f, i, j, k, l, g])
    }
}
/// n = 12, i = 3, b < f, b < l, c < i, c < l, d < e, d < g, d < i, d < l, g < h, i < j, i < k
fn select_1475([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < b {
        select_1467([a, g, e, c, h, b, i, j, k, f])
    } else {
        select_1474([a, b, c, d, f, g, h, e, i, j, k, l])
    }
}
/// n = 15, i = 4, a < e, a < i, b < i, b < l, c < d, c < f, c < o, f < g, f < h, f < l, h < j, i < k, i < o, l < m, l < n
fn select_1476([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if i < f {
        select_545([e, c, b, d, i, k, f, o])
    } else {
        select_1475([d, a, b, f, g, e, h, j, l, m, n, i])
    }
}
/// n = 16, i = 4, a < m, b < e, b < f, c < d, c < g, c < l, f < i, f < l, g < h, g < j, g < m, j < k, l < n, m < o, m < p
fn select_1477([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if f < a {
        select_1464([b, c, d, e, g, f, h, a, i, j, k, l, n])
    } else {
        select_1476([b, a, c, d, e, g, h, j, f, k, i, m, o, p, l])
    }
}
/// n = 12, i = 2, a < e, a < g, b < c, b < d, b < f, b < h, f < k, g < l, h < i, h < j
fn select_1478([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < a {
        select_566([c, d, f, h, a, i, j, k])
    } else {
        select_577([a, b, c, d, e, f, g, k, l, h])
    }
}
/// n = 12, i = 2, a < g, b < f, c < d, c < e, c < h, c < i, h < l, i < j, i < k
fn select_1479([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_1478([a, c, d, e, g, h, b, i, j, k, l, f])
    } else {
        select_1478([b, c, d, e, f, h, a, i, j, k, l, g])
    }
}
/// n = 12, i = 2, c < g, d < e, d < f, d < h, d < i, h < l, i < j, i < k
fn select_1480([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_1479([a, c, d, e, f, g, b, h, i, j, k, l])
    } else {
        select_1479([b, c, d, e, f, g, a, h, i, j, k, l])
    }
}
/// n = 11, i = 3, b < e, b < f, b < g, c < d, c < f, c < g, f < k, g < h, g < i, g < j
fn select_1481([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < e {
        select_499([a, d, b, f, g, h, i, j, k, e])
    } else {
        select_499([a, e, c, f, g, h, i, j, k, d])
    }
}
/// n = 16, i = 4, a < d, a < e, a < l, b < c, b < f, b < k, e < h, e < k, f < g, f < i, f < l, i < j, k < p, l < m, l < n, l < o
fn select_1482([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p]: [usize; 16]) -> usize {
    if e < f {
        select_1481([d, b, e, h, c, k, f, g, i, l, p])
    } else {
        select_1122([c, a, f, g, d, i, j, e, l, m, n, o, h, k])
    }
}
/// n = 17, i = 4, a < d, a < e, b < c, b < f, b < o, e < h, e < o, f < g, f < i, f < j, i < m, j < k, j < l, j < n, n < p, o < q
fn select_1483([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if j < a {
        select_1480([c, g, i, j, k, l, m, n, a, d, e, p])
    } else {
        select_1482([a, b, c, d, e, f, g, h, i, m, o, j, k, l, n, q])
    }
}
/// n = 17, i = 4, b < e, b < f, c < d, c < g, c < o, f < i, f < o, g < h, g < j, g < k, j < m, k < l, k < n, n < p, o < q
fn select_1484([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if a < k {
        select_1477([a, b, c, d, e, f, g, h, i, j, m, o, k, q, l, n])
    } else {
        select_1483([b, c, d, e, f, g, h, i, j, k, a, l, m, n, o, p, q])
    }
}
/// n = 8, i = 5, a < h, b < g, c < f, c < h, d < e, d < h, g < h
fn select_1485([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_1129([a, e, c, b, g, f, h])
    } else {
        select_1129([a, f, d, b, g, e, h])
    }
}
/// n = 10, i = 2, a < e, b < c, b < d, b < f, b < g, f < j, g < h, g < i
fn select_1486([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if g < a {
        select_566([c, d, f, g, a, h, i, j])
    } else {
        select_571([a, b, c, d, e, f, j, g])
    }
}
/// n = 7, i = 3, a < c, a < d, b < e, e < f, f < g
fn select_1487([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if e < c {
        select_90([a, e, d, f, g, c])
    } else {
        select_44([d, b, c, e])
    }
}
/// n = 9, i = 3, a < c, a < d, b < e, e < f, e < g, f < i, g < h
fn select_1488([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < c {
        select_364([a, e, d, f, g, h, i])
    } else {
        select_1487([a, b, c, d, e, g, h])
    }
}
/// n = 9, i = 3, a < c, a < d, b < e, e < f, e < g, e < h, h < i
fn select_1489([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < g {
        select_1488([a, b, c, d, e, f, h, i, g])
    } else {
        select_1488([a, b, c, d, e, g, h, i, f])
    }
}
/// n = 10, i = 3, a < c, a < i, a < j, b < d, c < e, d < f, d < i, d < j, f < g, f < h
fn select_1490([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < c {
        select_151([a, f, g, h, i, j])
    } else {
        select_237([c, b, e, d, i, j])
    }
}
/// n = 11, i = 3, a < c, a < j, a < k, b < d, c < e, d < f, d < g, d < j, d < k, f < i, g < h
fn select_1491([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < g {
        select_1490([a, b, c, d, e, f, g, i, j, k])
    } else {
        select_1490([a, b, c, d, e, g, f, h, j, k])
    }
}
/// n = 11, i = 3, a < c, a < j, a < k, b < d, c < g, d < e, d < f, d < h, d < j, d < k, h < i
fn select_1492([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_1491([a, b, c, d, g, e, h, i, f, j, k])
    } else {
        select_1491([a, b, c, d, g, f, h, i, e, j, k])
    }
}
/// n = 11, i = 3, a < d, b < j, b < k, c < e, e < f, e < g, e < h, e < j, e < k, h < i
fn select_1493([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < b {
        select_1489([a, c, b, d, e, f, g, h, i])
    } else {
        select_1492([b, c, a, e, f, g, d, h, i, j, k])
    }
}
/// n = 12, i = 3, a < l, b < d, c < e, e < f, e < g, e < h, e < i, e < l, h < k, i < j
fn select_1494([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < a {
        select_1486([b, e, f, g, d, i, h, a, k, j])
    } else {
        select_1493([b, a, c, d, e, f, g, i, j, h, l])
    }
}
/// n = 12, i = 3, c < l, d < e, e < f, e < g, e < h, e < i, e < l, h < k, i < j
fn select_1495([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if a < b {
        select_1494([c, a, d, b, e, f, g, h, i, j, k, l])
    } else {
        select_1494([c, b, d, a, e, f, g, h, i, j, k, l])
    }
}
/// n = 14, i = 5, a < g, b < h, c < f, c < h, d < e, d < h, h < i, h < j, h < k, h < l, k < n, l < m
fn select_1496([a, b, c, d, e, f, g, h, i, j, k, l, m, n]: [usize; 14]) -> usize {
    if g < h {
        select_1485([b, a, c, d, e, f, g, h])
    } else {
        select_1495([e, f, a, b, h, i, j, k, l, m, n, g])
    }
}
/// n = 8, i = 3, a < d, b < e, c < e, c < h, d < h, e < f, e < g
fn select_1497([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_44([b, c, d, h])
    } else {
        select_11([a, e, f, g])
    }
}
/// n = 10, i = 5, a < e, b < h, c < g, c < h, d < f, e < g, f < h, h < i, h < j
fn select_1498([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_1497([a, b, c, e, h, i, j, g])
    } else {
        select_384([b, c, d, f, g])
    }
}
/// n = 9, i = 4, a < f, b < f, c < g, d < e, e < g, g < h, g < i
fn select_1499([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < a {
        select_18([b, g, a, h, i])
    } else {
        select_1129([c, b, a, d, e, f, g])
    }
}
/// n = 10, i = 5, a < f, b < h, c < g, d < e, d < h, g < h, h < i, h < j
fn select_1500([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_1498([a, b, d, c, f, g, e, h, i, j])
    } else {
        select_1499([a, e, b, c, g, f, h, i, j])
    }
}
/// n = 11, i = 5, a < k, b < f, b < j, c < g, d < e, d < h, g < h, h < i, h < j, h < k
fn select_1501([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if a < h {
        select_1500([b, a, c, d, e, f, g, h, i, k])
    } else {
        select_1088([e, b, g, f, h, i, a, k, j])
    }
}
/// n = 7, i = 4, a < g, b < d, c < e, d < g, e < f
fn select_1502([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if d < f {
        select_96([a, d, c, e, g, f])
    } else {
        select_44([a, b, f, d])
    }
}
/// n = 9, i = 5, a < h, b < g, b < i, c < e, d < f, e < h, e < i, f < g, f < i
fn select_1503([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < a {
        select_405([a, b, c, g, e, i, h])
    } else {
        select_1502([b, d, c, f, e, h, g])
    }
}
/// n = 9, i = 5, a < h, b < f, c < e, c < i, d < g, f < i, g < h, g < i
fn select_1504([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < e {
        select_1503([a, c, d, b, g, f, e, h, i])
    } else {
        select_1439([a, b, d, c, g, e, f, h])
    }
}
/// n = 8, i = 5, a < h, b < f, c < e, d < g, g < h
fn select_1505([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if e < f {
        select_1439([a, b, d, c, g, e, f, h])
    } else {
        select_1439([a, c, d, b, g, f, e, h])
    }
}
/// n = 9, i = 5, a < f, b < h, c < g, d < e, d < i, g < i, h < i
fn select_1506([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if g < f {
        select_1504([a, b, d, c, e, h, g, f, i])
    } else {
        select_1505([c, b, d, a, e, h, f, g])
    }
}
/// n = 11, i = 5, a < g, b < f, b < k, c < h, d < e, d < i, h < i, i < j, i < k
fn select_1507([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if i < g {
        select_1501([a, b, c, d, e, f, h, i, j, k, g])
    } else {
        select_1506([b, a, c, d, e, f, h, g, i])
    }
}
/// n = 9, i = 5, a < h, b < g, b < i, c < e, d < f, e < g, f < h, h < i
fn select_1508([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < e {
        select_362([b, a, c, e, h, g, i])
    } else {
        select_406([a, b, d, g, f, h])
    }
}
/// n = 7, i = 3, a < g, b < e, c < d, c < f, d < g, e < f
fn select_1509([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if a < e {
        select_96([b, a, c, d, e, g])
    } else {
        select_19([c, e, a, d, f])
    }
}
/// n = 9, i = 5, a < g, b < h, c < f, d < e, d < i, e < g, f < h, h < i
fn select_1510([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < e {
        select_1509([a, b, d, e, h, i, g])
    } else {
        select_406([b, a, c, g, f, h])
    }
}
/// n = 9, i = 5, a < f, b < h, c < e, c < i, d < g, g < h, h < i
fn select_1511([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if f < e {
        select_1508([b, c, a, d, f, g, e, h, i])
    } else {
        select_1510([a, b, d, c, e, g, f, h, i])
    }
}
/// n = 10, i = 4, b < f, b < g, c < f, c < g, d < e, d < g, g < h, g < i, g < j
fn select_1512([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if f < e {
        select_606([a, f, d, g, h, i, j, e])
    } else {
        select_1135([a, e, b, c, g, h, i, j, f])
    }
}
/// n = 12, i = 5, a < f, b < h, b < i, c < e, c < i, d < g, g < h, g < i, i < j, i < k, i < l
fn select_1513([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if f < i {
        select_1505([b, a, c, d, e, f, g, h])
    } else {
        select_1512([a, b, g, c, e, h, i, j, k, l])
    }
}
/// n = 12, i = 5, a < g, b < h, c < f, c < i, d < e, d < i, h < i, i < j, i < k, i < l
fn select_1514([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < h {
        select_1511([a, b, c, d, f, g, e, h, i])
    } else {
        select_1513([a, d, c, b, f, g, h, e, i, j, k, l])
    }
}
/// n = 15, i = 5, a < g, a < i, b < f, b < k, c < e, c < k, c < o, d < h, h < i, h < k, i < j, i < o, k < l, k < m, k < n
fn select_1515([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if i < k {
        select_1507([b, c, d, a, g, e, f, h, i, j, o])
    } else {
        select_1514([a, d, b, c, e, f, g, h, k, l, m, n])
    }
}
/// n = 17, i = 5, a < g, a < i, b < f, b < j, c < e, c < j, c < q, d < h, d < j, h < i, i < l, i < q, j < k, j < m, j < n, m < p, n < o
fn select_1516([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if j < h {
        select_1496([a, d, b, c, e, f, g, j, h, k, m, n, o, p])
    } else {
        select_1515([a, b, c, d, e, f, g, h, i, l, j, k, m, n, q])
    }
}
/// n = 10, i = 2, a < g, a < j, b < e, b < f, c < d, c < h, c < j, h < i
fn select_1517([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < c {
        select_1032([a, b, e, f, g, c, d, h])
    } else {
        select_154([a, c, d, g, h, b, e, f, i, j])
    }
}
/// n = 9, i = 2, a < c, a < f, b < d, b < e, d < h, e < g, f < i
fn select_1518([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if d < f {
        select_364([a, b, c, d, e, g, h])
    } else {
        select_694([b, a, c, f, e, i, g])
    }
}
/// n = 10, i = 2, a < g, b < e, b < j, c < d, c < f, c < j, f < h, g < i
fn select_1519([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < a {
        select_910([b, c, d, e, f, a, h, g, j])
    } else {
        select_1518([c, a, d, b, g, f, i, e, h])
    }
}
/// n = 10, i = 2, b < g, c < f, c < j, d < e, d < h, d < j, h < i
fn select_1520([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if b < a {
        select_1517([c, b, d, e, a, g, f, h, i, j])
    } else {
        select_1519([a, c, d, e, f, h, b, i, g, j])
    }
}
/// n = 7, i = 2, a < g, b < e, c < d, c < g, e < f
fn select_1521([a, b, c, d, e, f, g]: [usize; 7]) -> usize {
    if b < c {
        select_42([a, c, e, f, d])
    } else {
        select_42([d, a, b, e, g])
    }
}
/// n = 8, i = 2, b < f, c < d, c < e, e < g, f < h
fn select_1522([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if a < e {
        select_1521([a, b, c, d, f, h, e])
    } else {
        select_631([b, c, d, f, e, a, g, h])
    }
}
/// n = 8, i = 3, a < f, b < e, b < g, c < d, c < f, c < g, g < h
fn select_1523([a, b, c, d, e, f, g, h]: [usize; 8]) -> usize {
    if d < e {
        select_1388([d, a, b, f, g, h, e])
    } else {
        select_966([a, c, b, e, f, g, h, d])
    }
}
/// n = 10, i = 3, a < f, a < h, b < e, b < g, c < d, c < f, c < g, c < h, g < i, h < j
fn select_1524([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if h < e {
        select_1522([d, b, a, f, h, g, j, i])
    } else {
        select_1523([a, b, c, d, e, f, g, i])
    }
}
/// n = 11, i = 3, a < h, b < e, b < i, b < k, c < d, c < f, c < h, c < i, f < g, f < k, i < j
fn select_1525([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if f < a {
        select_1297([d, b, f, g, e, a, i, h, j, k])
    } else {
        select_1524([a, b, c, d, e, h, i, f, j, g])
    }
}
/// n = 11, i = 3, b < f, b < i, b < k, c < d, c < e, c < g, c < i, g < h, g < k, i < j
fn select_1526([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if d < a {
        select_1520([e, d, g, b, f, h, a, i, j, k])
    } else {
        select_1525([a, b, c, e, f, g, h, d, i, j, k])
    }
}
/// n = 10, i = 2, c < d, c < e, c < f, e < i, e < j, f < g, f < h
fn select_1527([a, b, c, d, e, f, g, h, i, j]: [usize; 10]) -> usize {
    if e < f {
        select_34([a, b, c, d, e, f, i, j])
    } else {
        select_34([a, b, c, d, f, e, g, h])
    }
}
/// n = 11, i = 2, c < d, c < e, c < f, c < g, e < k, f < j, g < h, g < i
fn select_1528([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < f {
        select_1527([a, b, c, d, e, g, h, i, f, k])
    } else {
        select_1527([a, b, c, d, f, g, h, i, e, j])
    }
}
/// n = 9, i = 2, c < d, c < e, c < f, f < g, f < h, f < i
fn select_1529([a, b, c, d, e, f, g, h, i]: [usize; 9]) -> usize {
    if a < b {
        select_623([a, c, d, e, b, f, g, h, i])
    } else {
        select_623([b, c, d, e, a, f, g, h, i])
    }
}
/// n = 11, i = 4, a < e, a < f, b < g, c < f, c < g, d < e, d < g, g < h, g < i, g < j, g < k
fn select_1530([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if g < a {
        select_22([a, h, i, j, k])
    } else {
        select_255([b, c, d, e, f, g])
    }
}
/// n = 11, i = 4, a < f, b < g, c < f, c < g, d < e, d < g, g < h, g < i, g < j, g < k
fn select_1531([a, b, c, d, e, f, g, h, i, j, k]: [usize; 11]) -> usize {
    if e < a {
        select_729([e, b, c, a, g, h, i, j, k, f])
    } else {
        select_1530([a, b, c, d, e, f, g, h, i, j, k])
    }
}
/// n = 12, i = 5, a < h, b < g, b < h, c < f, c < h, d < e, d < h, h < i, h < j, h < k, h < l
fn select_1532([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if e < f {
        select_1531([e, a, c, b, g, f, h, i, j, k, l])
    } else {
        select_1531([f, a, d, b, g, e, h, i, j, k, l])
    }
}
/// n = 12, i = 5, a < g, a < k, a < l, b < h, c < f, c < h, d < e, d < h, h < i, h < j, h < k, h < l
fn select_1533([a, b, c, d, e, f, g, h, i, j, k, l]: [usize; 12]) -> usize {
    if h < a {
        select_1529([e, f, h, i, j, a, g, k, l])
    } else {
        select_1532([b, a, c, d, e, f, g, h, i, j, k, l])
    }
}
/// n = 15, i = 5, a < g, a < k, a < o, b < h, b < k, c < f, c < h, c < k, d < e, d < h, d < k, h < i, h < j, h < o, k < l, k < m, k < n
fn select_1534([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o]: [usize; 15]) -> usize {
    if h < k {
        select_1533([a, b, c, d, e, f, g, h, i, j, k, o])
    } else {
        select_1532([b, a, c, d, e, f, g, k, h, l, m, n])
    }
}
/// n = 17, i = 5, a < g, a < h, b < f, b < i, b < q, c < h, c < i, d < e, d < h, d < i, h < k, h < l, h < q, i < j, i < m, i < n, m < p, n < o
fn select_1535([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q]: [usize; 17]) -> usize {
    if i < a {
        select_1528([e, f, i, j, m, n, a, g, h, o, p])
    } else {
        select_1534([b, c, a, d, e, g, f, h, k, l, i, j, m, n, q])
    }
}
/// n = 18, i = 5, a < g, a < h, b < f, b < k, c < e, c < k, c < o, d < h, d < k, h < i, h < j, h < o, k < l, k < m, k < n, m < q, n < p, o < r
fn select_1536([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if h < b {
        select_1526([g, c, h, i, j, e, b, f, o, r, k])
    } else {
        select_1535([a, c, d, b, f, e, g, h, k, l, i, j, m, n, p, q, o])
    }
}
/// n = 18, i = 5, a < h, a < i, b < g, b < k, c < f, c < k, c < o, d < e, d < i, d < k, i < j, i < o, k < l, k < m, k < n, m < q, n < p, o < r
fn select_1537([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if e < i {
        select_1516([a, b, c, d, f, g, h, e, i, k, l, j, m, n, p, q, o])
    } else {
        select_1536([a, b, c, d, f, g, h, i, e, j, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, a < h, a < p, b < g, b < i, c < f, c < j, c < o, d < e, d < i, d < j, i < l, i < o, j < k, j < m, j < p, m < n, o < q, p < r
fn select_1538([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if j < a {
        select_1484([e, b, c, f, g, i, j, k, l, m, a, h, n, p, o, r, q])
    } else {
        select_1537([b, a, c, d, e, f, h, g, i, l, j, k, m, p, o, r, n, q])
    }
}
/// n = 18, i = 5, a < h, a < i, b < g, b < l, c < f, c < k, c < q, d < e, d < k, d < l, i < j, k < m, k < o, l < n, l < q, o < p, q < r
fn select_1539([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if i < k {
        select_1446([b, c, a, d, e, h, f, g, i, j, l, n, q, k, m, o, r])
    } else {
        select_1538([a, b, c, d, e, f, g, h, l, k, m, n, o, p, q, i, r, j])
    }
}
/// n = 18, i = 5, a < j, b < i, c < h, c < l, d < g, d < k, d < q, e < f, e < k, e < l, k < m, k < o, l < n, l < q, o < p, q < r
fn select_1540([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1539([a, c, d, e, f, g, h, j, b, i, k, l, m, n, o, p, q, r])
    } else {
        select_1539([b, c, d, e, f, g, h, i, a, j, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, a < j, b < i, c < h, d < g, d < m, d < p, e < f, e < k, e < m, k < l, k < p, m < n, m < o, o < q, p < r
fn select_1541([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if k < b {
        select_1346([a, c, d, e, f, g, h, j, k, l, b, m, i, n, o, p, q, r])
    } else {
        select_1540([a, c, b, d, e, f, g, i, h, j, m, k, n, l, o, q, p, r])
    }
}
/// n = 18, i = 5, c < j, d < i, e < h, e < m, e < p, f < g, f < k, f < m, k < l, k < p, m < n, m < o, o < q, p < r
fn select_1542([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1541([a, c, d, e, f, g, h, i, j, b, k, l, m, n, o, p, q, r])
    } else {
        select_1541([b, c, d, e, f, g, h, i, j, a, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, e < j, f < i, f < m, f < p, g < h, g < k, g < m, k < l, k < p, m < n, m < o, o < q, p < r
fn select_1543([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1542([c, d, a, e, f, g, h, i, j, b, k, l, m, n, o, p, q, r])
    } else {
        select_1542([c, d, b, e, f, g, h, i, j, a, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, g < j, g < m, g < p, h < i, h < k, h < m, k < l, k < p, m < n, m < o, o < q, p < r
fn select_1544([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1543([c, d, e, f, a, g, h, i, j, b, k, l, m, n, o, p, q, r])
    } else {
        select_1543([c, d, e, f, b, g, h, i, j, a, k, l, m, n, o, p, q, r])
    }
}
/// n = 18, i = 5, g < j, g < l, g < o, h < i, h < k, h < o, k < m, l < n, o < p, o < q, q < r
fn select_1545([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if k < l {
        select_1544([a, b, c, d, e, f, g, h, i, j, k, m, o, p, q, l, r, n])
    } else {
        select_1544([a, b, c, d, e, f, h, g, j, i, l, n, o, p, q, k, r, m])
    }
}
/// n = 18, i = 5, g < j, g < l, h < i, h < k, h < m, k < o, l < p, m < n, m < q, q < r
fn select_1546([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if m < g {
        select_1148([a, b, c, d, e, f, h, i, k, m, n, o, q, g, j, r, l, p])
    } else {
        select_1545([a, b, c, d, e, f, g, h, i, j, k, l, o, p, m, n, q, r])
    }
}
/// n = 18, i = 5, g < l, h < k, i < j, i < m, i < n, m < p, n < o, n < q, q < r
fn select_1547([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if g < h {
        select_1546([a, b, c, d, e, f, g, i, j, l, m, h, n, o, p, k, q, r])
    } else {
        select_1546([a, b, c, d, e, f, h, i, j, k, m, g, n, o, p, l, q, r])
    }
}
/// n = 18, i = 5, g < n, h < m, i < l, i < p, j < k, j < o, o < q, p < r
fn select_1548([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if i < j {
        select_1547([a, b, c, d, e, f, g, h, i, l, m, n, p, j, k, r, o, q])
    } else {
        select_1547([a, b, c, d, e, f, g, h, j, k, m, n, o, i, l, q, p, r])
    }
}
/// n = 18, i = 5, g < p, h < o, i < n, j < m, k < l, k < q, q < r
fn select_1549([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if i < j {
        select_1548([a, b, c, d, e, f, g, h, i, k, l, n, o, p, q, j, r, m])
    } else {
        select_1548([a, b, c, d, e, f, g, h, j, k, l, m, o, p, q, i, r, n])
    }
}
/// n = 18, i = 5, i < p, j < o, k < n, l < m, l < q, q < r
fn select_1550([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1549([c, d, e, f, g, h, a, i, j, k, l, m, n, o, p, b, q, r])
    } else {
        select_1549([c, d, e, f, g, h, b, i, j, k, l, m, n, o, p, a, q, r])
    }
}
/// n = 18, i = 5, k < p, l < o, m < n, m < q, q < r
fn select_1551([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1550([c, d, e, f, g, h, i, j, a, k, l, m, n, o, p, b, q, r])
    } else {
        select_1550([c, d, e, f, g, h, i, j, b, k, l, m, n, o, p, a, q, r])
    }
}
/// n = 18, i = 5, m < p, n < o, n < q, q < r
fn select_1552([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1551([c, d, e, f, g, h, i, j, k, l, a, m, n, o, p, b, q, r])
    } else {
        select_1551([c, d, e, f, g, h, i, j, k, l, b, m, n, o, p, a, q, r])
    }
}
/// n = 18, i = 5, o < p, o < q, q < r
fn select_1553([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1552([c, d, e, f, g, h, i, j, k, l, m, n, a, o, p, b, q, r])
    } else {
        select_1552([c, d, e, f, g, h, i, j, k, l, m, n, b, o, p, a, q, r])
    }
}
/// n = 18, i = 5, o < r, p < q
fn select_1554([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if o < p {
        select_1553([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, r, p, q])
    } else {
        select_1553([a, b, c, d, e, f, g, h, i, j, k, l, m, n, p, q, o, r])
    }
}
/// n = 18, i = 5, q < r
fn select_1555([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1554([c, d, e, f, g, h, i, j, k, l, m, n, o, p, a, q, r, b])
    } else {
        select_1554([c, d, e, f, g, h, i, j, k, l, m, n, o, p, b, q, r, a])
    }
}
/// n = 18, i = 5
fn select_0([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r]: [usize; 18]) -> usize {
    if a < b {
        select_1555([c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, a, b])
    } else {
        select_1555([c, d, e, f, g, h, i, j, k, l, m, n, o, p, q, r, b, a])
    }
}
